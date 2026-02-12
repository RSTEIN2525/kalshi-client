from ..kalshi.models import Candlestick, UnwrappedCandlestick
from ..technical_analysis import Data

def unwrap_candlestick(candlestick: Candlestick) -> UnwrappedCandlestick:

    # Pydantic -> Dictionary
    c = candlestick.model_dump()

    return UnwrappedCandlestick(
        end_period_ts=c["end_period_ts"],
        **{f"yes_bid_{k}": v for k, v in c["yes_bid"].items()},
        **{f"yes_ask_{k}": v for k, v in c["yes_ask"].items()},
        **{f"price_{k}": v for k, v in c["price"].items()},
        volume=c["volume"],
        volume_fp=c["volume_fp"],
        open_interest=c["open_interest"],
        open_interest_fp=c["open_interest_fp"],
    )

def unwrap_candlesticks(candlesticks: list[Candlestick]) -> list[UnwrappedCandlestick]:

    # Pydantic -> Dictionary
    c:list[UnwrappedCandlestick] = []

    for candlestick in candlesticks:
        c.append(unwrap_candlestick(candlestick))
    
    return c


def _to_float(val) -> float:
    return float(val) if val is not None else float('nan')

def kalshi_candlestick_to_ta_data(candlestick: UnwrappedCandlestick, period_interval: int) -> Data:

    c = candlestick.model_dump()

    end_ts = c["end_period_ts"]
    start_ts = end_ts - period_interval * 60

    ask = _to_float(c["yes_ask_close_dollars"])
    bid = _to_float(c["yes_bid_close_dollars"])

    return Data(
        start_ts= start_ts,
        end_ts= end_ts,
        open= _to_float(c["price_open_dollars"]),
        high= _to_float(c["price_high_dollars"]),
        low= _to_float(c["price_low_dollars"]),
        close= _to_float(c["price_close_dollars"]),
        volume= _to_float(c["volume_fp"]),
        ask= ask,
        bid= bid,
        spread= ask - bid,
        midprice= (ask + bid) / 2,
        open_interest= _to_float(c["open_interest_fp"])
    )

def to_ta_data(candlesticks: list[UnwrappedCandlestick], period_interval: int) -> list[Data]:

    d : list[Data] = []

    for candlestick in candlesticks:
        d.append(kalshi_candlestick_to_ta_data(candlestick, period_interval))

    return d