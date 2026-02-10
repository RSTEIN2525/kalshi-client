from datetime import datetime,timezone
from ..kalshi.models import Market

# ISO 8601 string -> Unix timestamp
def iso_to_unix(iso_string: str) -> int:
    dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
    return int(dt.timestamp())

def get_start_ts(markets: list[Market]) -> int:
    market_start_times = [datetime.fromisoformat(market.open_time.replace("Z", "+00:00")) for market in markets]
    return int(min(market_start_times).timestamp())


def get_end_ts(markets: list[Market]) -> int:
     market_end_times   = [datetime.fromisoformat(market.close_time.replace("Z", "+00:00")) for market in markets]
     return int(max(market_end_times).timestamp())
