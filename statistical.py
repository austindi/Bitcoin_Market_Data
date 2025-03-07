from numpy.typing import NDArray
import numpy as np 


def moving_average(prices: np.ndarray ) -> float:
    return np.average(prices )

# Calculate RSI (Relative Strength Index)
def RSI(prices: np.ndarray, period: int = 14) -> float:
    """Computes RSI for the last 'period' days only."""
    if len(prices) < period:
        raise ValueError(f"Not enough data! Need at least {period} days.")
    
    # Compute daily price differences
    deltas = np.diff(prices[-(period + 1):])  # Only consider last (14+1) days
    
    # Separate gains and losses
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)

    # Compute average gain/loss
    avg_gain = np.mean(gains)
    avg_loss = np.mean(losses)

    # Avoid division by zero
    if avg_loss == 0:
        return 100.0  # RSI is maxed out

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

# Calculate Sharpe Ratio
def Sharpe_Ratio(prices: np.ndarray, period: int = 90, risk_free_rate: float = 0.03) -> float:
    """Computes Sharpe Ratio using the last 'period' days of data."""
    if len(prices) < period:
        raise ValueError(f"Not enough data! Need at least {period} days.")

    # Compute daily returns (percentage change)
    returns = np.diff(prices[-(period + 1):]) / prices[-(period + 1):-1]

    # Compute Sharpe Ratio
    excess_return = np.mean(returns) - (risk_free_rate / 252)  # Convert annual risk-free rate to daily
    volatility = np.std(returns)

    return excess_return / volatility if volatility != 0 else np.nan

def find_average( json_obj : dict , name : str ) -> int: 
    quant = [] 
    for exchange in json_obj: 
        quant.append( float( exchange[ name ]  ) )
    return np.average( np.array( quant ) )  
