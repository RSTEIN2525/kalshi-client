import pandas as pd
import pandas_ta as ta

def crossover(a: pd.Series, b: pd.Series) -> pd.Series:
    return (a > b) & (a.shift(1) <= b)

def crossunder(a: pd.Series, b: pd.Series) -> pd.Series:
    return (a < b) & (a.shift(1) >= b)

def const_to_series(val, len) -> pd.Series:
    s = pd.Series(val, index=range(len))
    return s