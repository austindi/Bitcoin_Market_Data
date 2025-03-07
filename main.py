import pendulum
import os 
from prefect import task, flow, get_run_logger 
import duckdb 
import requests 
from dotenv import load_dotenv
from statistical import * 
import json
from datetime import datetime, UTC

nyc_time = pendulum.timezone("America/New_York")

@task( name = "Data transformation" )  
def transform_data( json_obj : dict, derivates_dict : dict ) -> dict: 
    logger = get_run_logger()
    #Turning JSON object into numpy arrays of prices and dates 
    timestamps = np.array([entry[0] for entry in json_obj["prices"]])  # Unix timestamps
    prices = np.array([entry[1] for entry in json_obj["prices"]])  # Closing prices
    dates = np.array([datetime.fromtimestamp(ts / 1000, UTC) for ts in timestamps])
   
    #Calculating Statistical metrics 
    mov_avg_50_day = moving_average( prices[ -50: ] )
    mov_avg_200_day = moving_average( prices )
    rsi = RSI( prices, 14 )
    sharpe_ratio = Sharpe_Ratio( prices )
    avg_trade_vol = find_average( derivates_dict , 'trade_volume_24h_btc' )   

    #Turning data into a crypo dataclass 
    crypto_data = { 'RSI': rsi, 'Sharpe_Ratio': sharpe_ratio, 'MA_200' :mov_avg_200_day, 'MA_50':mov_avg_50_day, 'price' : prices[ -1 ], "24h_trade_volume": avg_trade_vol }  
    logger.info( 'Statistical procedures complete!' ) 
    logger.info( crypto_data ) 
    return crypto_data 

@task(retries=3, retry_delay_seconds=5, name = "Making API call" )
def collect_info( API_KEY: str ,  URL: str, params : dict = {} )-> dict: 
    #API calls are made 
    logger = get_run_logger()
    headers = { "x-cg-demo-api-key": API_KEY  }
    response = requests.get(URL, headers=headers, params = params)

    #Check to see if API Call was successful 
    if response.status_code == 200:
        logger.info("Successfully retrived data from API" )
        
    else:
        logger.error( f"Error retriving data from API: {response.status_code}: {response.text}")

    return  response.json()


@task( name = 'Adding data to database' ) 
def add_data_to_DB(data_base: str, crypto_dict: dict) -> None:
    logger = get_run_logger() 

    db_path = f"database/{data_base}"
    #Check to see if the database folder exist and creates it if it doesn't 
    if not os.path.exists("database"):
        logger.warning( 'Database folder was not found! Creating one now.' ) 
        os.mkdir("database")
   
    # Makes table for the data 
    with duckdb.connect(db_path) as con:
        logger.info( 'Connected to database.' ) 
        con.execute("""
            CREATE TABLE IF NOT EXISTS crypto_data (
                id BIGINT PRIMARY KEY, 
                timestamp TIMESTAMP DEFAULT NOW(),
                price FLOAT,
                MA_50_day FLOAT,
                MA_200_day FLOAT,
                Sharpe_Ratio FLOAT,
                RSI FLOAT,
                Trade_volume_24h FLOAT
            )
        """)

        query = """
            INSERT INTO crypto_data (id, timestamp, price, MA_50_day, MA_200_day, Sharpe_Ratio, RSI, Trade_volume_24h)
            SELECT COALESCE(MAX(id), 0) + 1, NOW(), ?, ?, ?, ?, ?, ?
            FROM crypto_data
        """

        con.execute(query, (
            crypto_dict["price"], 
            crypto_dict["MA_50"],
            crypto_dict["MA_200"],
            crypto_dict["Sharpe_Ratio"],
            crypto_dict["RSI"],
            crypto_dict["24h_trade_volume"] ))
        logger.info('Crypto data added to database.' ) 

@flow
def collect_market_data( )-> None:  

    load_dotenv()
    API_KEY = os.getenv("MY_API_KEY")
    URL =  "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"

    params = { "vs_currency": "usd","days": 200 }
    coin_data = collect_info( API_KEY, URL = URL, params = params ) 

    URL = "https://api.coingecko.com/api/v3/derivatives/exchanges"
    params = {} 
    derivates_data = collect_info( API_KEY =API_KEY ,  URL = URL )

    crypto_object = transform_data( coin_data , derivates_data )  
     
    add_data_to_DB('bitcoin.db', crypto_object)


if __name__ == '__main__':
    #Runs at 9:30 EST/14:30 UTC  
    collect_market_data.serve(
        name="bitcoin-data-deployment", cron="30 14 * * *" )
