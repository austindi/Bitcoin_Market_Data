from numpy.typing import NDArray
from dotenv import load_dotenv
import os 
import smtplib
import numpy as np 


def get_SMTP( ):
     SMTP = { }
     load_dotenv()
     SMTP[ 'server' ]   = os.getenv( "mail_server" ) 
     SMTP[ 'port' ]     = int( os.getenv( "mail_port" ) )
     SMTP[ 'username' ] = os.getenv( "mail_login" )  
     SMTP[ 'password' ] = os.getenv( "mail_password" ) 
     return SMTP

def send_email ( fromaddr, toaddrs, subject,  message, SMTP = get_SMTP( )):
    server = smtplib.SMTP( SMTP[ 'server' ], SMTP[ 'port' ] )
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login( SMTP[ 'username' ], SMTP[ 'password' ] )
    email_body = f"Subject: {subject}\nFrom: {fromaddr}\nTo: {toaddrs}\n\n{message}"
    server.sendmail(fromaddr, toaddrs,  email_body)
    server.quit()


def moving_average(prices: np.ndarray ) -> float:
    return np.average(prices )


def RSI(prices: np.ndarray, period: int = 14) -> float:
    
    deltas = np.diff(prices[-(period + 1):]) 
    

    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)


    avg_gain = np.mean(gains)
    avg_loss = np.mean(losses)


    if avg_loss == 0:
        return 100.0  

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi


def Sharpe_Ratio(prices: np.ndarray, period: int = 90, risk_free_rate: float = 0.03) -> float:
 
    returns = np.diff(prices[-(period + 1):]) / prices[-(period + 1):-1]

    excess_return = np.mean(returns) - (risk_free_rate / 252) 
    volatility = np.std(returns)

    return excess_return / volatility if volatility != 0 else np.nan


def find_average( json_obj : dict , name : str ) -> int: 
    quant = [] 
    for exchange in json_obj: 
        quant.append( float( exchange[ name ]  ) )
    return np.average( np.array( quant ) )  
