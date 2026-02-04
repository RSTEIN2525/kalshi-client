import requests
from .models import Series, PriceRange, MVESelectedLeg, Market, MarketsResponse

'''
KALSHI Semantics: Series v.s. Event v.s. Markets

Series (Template)
  └── Event (Specific instance)
       └── Market (Tradeable yes/no contract)
       └── Market (Another outcome)
       └── Market (Another outcome)

Real Example:

Series: "KXHIGHNY" (NYC Daily High Temperature)
Event: "High temp on Feb 4, 2026"
Markets:
    "Will it be 70°F or higher?"
    "Will it be 75°F or higher?"
    "Will it be 80°F or higher?"
'''

class KalshiClient:

    API_KEY:str

    def __init__(self, API_KEY):
        self.API_KEY = API_KEY

    def get_series(self, series_ticker:str) -> Series:
        
        # Insert Series into Base URL Format
        url = f"https://api.elections.kalshi.com/trade-api/v2/series/{series_ticker}"

        # Call HTTP Endpoint, and Parse to JSON
        response = requests.get(url)
        series_data = response.json()

        series_data = series_data['series']  # Remove Outer Nesting
        
        # Unpack into Pydantic Model
        series = Series(**series_data)

        return series
    
    def get_open_markets_general(self, limit = 100, status = "open") -> MarketsResponse:

        # Join URL params after first w/ &
        url = f"https://api.elections.kalshi.com/trade-api/v2/markets?limit={limit}&status={status}"

        # Fetch and parse to JSON
        response = requests.get(url)
        response_data = response.json()

        # No need to iterate through and pull field by field, can unpack via pydantic
        markets_response = MarketsResponse(**response_data)

        return markets_response
    
    def get_single_market(self, ticker) -> Market:
        
        url = "https://api.elections.kalshi.com/trade-api/v2/markets/{ticker}"

        # Pull
        response = requests.get(url)

        # Serialize
        data = response.json()

        # Unpack
        market = Market(**data)

        return market
    

    def get_market_candle_sticks(self, series_ticker, market_ticker, start_ts, end_ts, period_interval, include_latest_before_start=False)
    '''
    @params
    series_ticker: Series ticker - the series that contains the target market
    market_ticker: Market ticker - unique identifier for the specific market
    start_ts: Start timestamp (Unix timestamp). Candlesticks will include those ending on or after this time.
    end_ts: End timestamp (Unix timestamp). Candlesticks will include those ending on or before this time.
    period_interval: Time period length of each candlestick in minutes. Valid values are 1 (1 minute), 60 (1 hour), or 1440 (1 day).
    included_latest_before_start: In cur candle(not closed) append a final synthetic candle to series "imagining" current price as a 'close' for cur
    
    '''


