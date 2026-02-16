import plotext as plo
import pandas as pd
from .time import unix_to_datestr

def plot_rsi(df: pd.DataFrame, title:str):
    candle_df = df.dropna(subset=["open", "close", "high", "low"])
    dates = [unix_to_datestr(ts) for ts in candle_df["end_ts"]]
    data = {
        "Open": candle_df["open"].tolist(),
        "Close": candle_df["close"].tolist(),
        "High": candle_df["high"].tolist(),
        "Low": candle_df["low"].tolist(),
    }

    plo.subplots(2, 1)

    # Top: Candlestick chart
    plo.subplot(1, 1)
    plo.candlestick(dates, data)
    plo.title(title)

    # Bottom: RSI
    plo.subplot(2, 1)
    plo.plot(df['rsi'].tolist())
    plo.plot([50] * len(df), label="midline")
    plo.title("RSI")

    plo.show()