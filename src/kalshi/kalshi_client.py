import requests
from .models import Series, PriceRange, MVESelectedLeg, Market, MarketsResponse, TagList, SeriesList,EventsResponse, Event, EventResponse,  Candlestick, CandlestickOHLC, CandlestickPriceOHLC, EventCandlesticksResponse
from ..trading_constants import DEFAULT_TIMEFRAME
from ..utils import pydantic_model_to_dataframe, iso_to_unix, get_end_ts, get_start_ts

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

    API_KEY: str

    def __init__(self, API_KEY):
        self.API_KEY = API_KEY

    def get_tags_by_categories(self) -> TagList:
        url = "https://api.elections.kalshi.com/trade-api/v2/search/tags_by_categories"

        response = requests.get(url)

        data = response.json()

        tags = TagList(**data)

        return tags
    
    def get_series(self, series_ticker: str, include_volume=True) -> Series:

        # Insert Series into Base URL Format
        url = f"https://api.elections.kalshi.com/trade-api/v2/series/{series_ticker}"

        # Call HTTP Endpoint, and Parse to JSON
        response = requests.get(url, params={"include_volume": include_volume})
        series_data = response.json()

        series_data = series_data['series']  # Remove Outer Nesting

        # Unpack into Pydantic Model
        series = Series(**series_data)

        return series

    def get_series_list(self, category=None, tags=None, include_product_metadata=False, include_volume=True):

        params = {}

        params["include_volume"] = include_volume
        params["include_product_metadata"] = include_product_metadata

        if category:
            params["category"] = category

        if tags:
            params["tags"] = tags

        url = "https://api.elections.kalshi.com/trade-api/v2/series"

        response = requests.get(url, params=params)

        data = response.json()

        series = SeriesList(**data)

        return series

    def get_open_markets_general(self, limit=100, status="open") -> MarketsResponse:

        # Join URL params after first w/ &
        url = f"https://api.elections.kalshi.com/trade-api/v2/markets?limit={limit}&status={status}"

        # Fetch and parse to JSON
        response = requests.get(url)
        response_data = response.json()

        # No need to iterate through and pull field by field, can unpack via pydantic
        markets_response = MarketsResponse(**response_data)

        return markets_response

    def get_markets_from_series_ticker(self, series_ticker,  limit=1000, status="open"):
        # Join URL params after first w/ &
        url = f"https://api.elections.kalshi.com/trade-api/v2/markets?limit={limit}&status={status}"

        # Fetch and parse to JSON
        response = requests.get(url, params={
            "series_ticker": series_ticker
        })
        response_data = response.json()

        # No need to iterate through and pull field by field, can unpack via pydantic
        markets_response = MarketsResponse(**response_data)

        return markets_response

    def get_single_market_from_market_ticker(self, market_ticker) -> Market:

        url = f"https://api.elections.kalshi.com/trade-api/v2/markets/{market_ticker}"

        # Pull
        response = requests.get(url)

        # Serialize
        data = response.json()

        # Unpack
        market = Market(**data)

        return market

    def get_market_candle_sticks(self, series: Series, market: Market, period_interval=DEFAULT_TIMEFRAME, include_latest_before_start=True):
        '''
        @params
        series_ticker: Series ticker - the series that contains the target market
        market_ticker: Market ticker - unique identifier for the specific market
        start_ts: Start timestamp (Unix timestamp). Candlesticks will include those ending on or after this time.
        end_ts: End timestamp (Unix timestamp). Candlesticks will include those ending on or before this time.
        period_interval: Time period length of each candlestick in minutes. Valid values are 1 (1 minute), 60 (1 hour), or 1440 (1 day).
        included_latest_before_start: In cur candle(not closed) append a final synthetic candle to series "imagining" current price as a 'close' for cur

        '''

        # Extract URL Parameters (Market, Series may not have TICKER)
        series_ticker = getattr(series, 'ticker', None)
        market_ticker = getattr(market, 'ticker', None)

        if not series_ticker or not market_ticker:
            print(
                f"Skipping Series-{series_ticker if series_ticker is not None else "DNE"} : Market-{market_ticker if market_ticker is not None else "DNE"}")
            return None

        url = f"https://api.elections.kalshi.com/trade-api/v2/series/{series_ticker}/markets/{market_ticker}/candlesticks"

        response = requests.get(url, params={
            "start_ts": iso_to_unix(market.open_time),
            "end_ts": iso_to_unix(market.close_time),
            "period_interval": period_interval,
            "include_latest_before_start": include_latest_before_start
        })

        parsed = response.json()
        print(parsed)

    def get_events(self, limit=100, status="open", series_ticker=None, with_milestones=True) -> EventsResponse:
        '''Batch Introduction to Event Data: Nothing on Volume, Inner Markets, ...'''

        url = f"https://api.elections.kalshi.com/trade-api/v2/events?limit={limit}"

        response = requests.get(url,params={
            "status" : status,
            "series_ticker": series_ticker,
            "with_milestones": with_milestones
        })

        raw =  response.json()

        events = EventsResponse(**raw)

        return events
    
    def get_event(self, event_ticker) -> EventResponse:
        '''More Specific Single Event -> All Markets Detailed Data'''

        with_nested_markets=True

        url = f"https://api.elections.kalshi.com/trade-api/v2/events/{event_ticker}"
        
        response = requests.get(url, params={
            "with_nested_markets": with_nested_markets
        })

        raw = response.json()

        event = EventResponse(**raw)

        return event
    

    def get_event_candle_sticks(self, event:Event, period_interval= DEFAULT_TIMEFRAME):

        series_ticker = event.series_ticker
        event_ticker = event.event_ticker

        start_ts = get_start_ts(event.markets)
        end_ts = get_end_ts(event.markets)

        url = f"https://api.elections.kalshi.com/trade-api/v2/series/{series_ticker}/events/{event_ticker}/candlesticks"

        response = requests.get(url, params={
            "start_ts" : start_ts,
            "end_ts" : end_ts,
            "period_interval" : period_interval 
        })

        raw = response.json()

        candles = EventCandlesticksResponse(**raw)

        return candles

    


if __name__ == '__main__':
    kc = KalshiClient("fake")
    # series_list = kc.get_series_list()

    # df = pydantic_model_to_dataframe(series_list.series)
    # df = df.sort_values(by='volume', ascending=False)
    # print(df)

    events = kc.get_events(limit=10)
    df = pydantic_model_to_dataframe(events.events)
    print(df)



    



    # df = pydantic_model_to_dataframe(markets.markets)
    # df.sort_values(by='volume')

    # print(df)



    # for market in markets.markets:

    #     # open = getattr(market, "open_time", "DONT HAVE")
    #     # print(open)

    #     candle_sticks = kc.get_market_candle_sticks(series, market)
