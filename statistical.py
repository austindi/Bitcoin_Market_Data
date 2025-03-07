from numpy.typing import NDArray
import numpy as np 


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
