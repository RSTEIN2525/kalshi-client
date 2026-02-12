from pydantic import BaseModel
from typing import Optional

class Series(BaseModel):
    ticker: str                                          # Unique identifier (e.g., "KXHIGHNY", "INX")
    frequency: str                                       # How often events occur ("daily", "weekly", "monthly")
    title: str                                           # Human-readable name
    category: str                                        # Market category (e.g., "Economics", "Weather", "Politics")
    tags: Optional[list[str]] = None                     # Keywords for filtering/search
    settlement_sources: Optional[list[dict[str, str]]] = None  # Where official data comes from to settle markets
    contract_url: str                                    # Link to contract details
    fee_type: str                                        # Fee structure type (typically "quadratic")
    fee_multiplier: float                                # Multiplier for fee calculation
    additional_prohibitions: Optional[list[str]] = None  # Extra trading restrictions
    product_metadata: Optional[dict] = None              # Custom metadata specific to this series
    volume: Optional[int] = None                         # Total trading volume (in cents)
    volume_fp: Optional[str] = None                      # Trading volume as decimal (in dollars)

class SeriesList(BaseModel):
    series: list[Series]

class PriceRange(BaseModel):
    start: str                                           # Start of price range
    end: str                                             # End of price range
    step: str                                            # Price increment step


class MVESelectedLeg(BaseModel):
    event_ticker: str                                    # Event identifier for this leg
    market_ticker: str                                   # Market identifier for this leg
    side: str                                            # Side of the position
    yes_settlement_value_dollars: Optional[str] = None   # Settlement value in dollars


class Market(BaseModel):
    ticker: str                                          # Unique market identifier
    event_ticker: str                                    # Associated event identifier
    market_type: str                                     # Type of market (e.g., "binary")
    title: str                                           # Market title
    subtitle: str                                        # Market subtitle
    yes_sub_title: str                                   # Yes outcome subtitle
    no_sub_title: str                                    # No outcome subtitle
    created_time: str                                    # ISO 8601 timestamp of market creation
    updated_time: str                                    # ISO 8601 timestamp of last update
    open_time: str                                       # ISO 8601 timestamp when market opened
    close_time: str                                      # ISO 8601 timestamp when market closes
    expiration_time: str                                 # ISO 8601 timestamp of expiration
    latest_expiration_time: str                          # ISO 8601 timestamp of latest possible expiration
    settlement_timer_seconds: int                        # Seconds until settlement
    status: str                                          # Market status (e.g., "initialized", "active", "settled")
    response_price_units: str                            # Price unit (e.g., "usd_cent")
    yes_bid: int                                         # Current yes bid price in cents
    yes_bid_dollars: str                                 # Current yes bid price in dollars
    yes_ask: int                                         # Current yes ask price in cents
    yes_ask_dollars: str                                 # Current yes ask price in dollars
    no_bid: int                                          # Current no bid price in cents
    no_bid_dollars: str                                  # Current no bid price in dollars
    no_ask: int                                          # Current no ask price in cents
    no_ask_dollars: str                                  # Current no ask price in dollars
    last_price: int                                      # Last traded price in cents
    last_price_dollars: str                              # Last traded price in dollars
    volume: int                                          # Total volume traded
    volume_fp: str                                       # Total volume as decimal
    volume_24h: int                                      # 24-hour trading volume
    volume_24h_fp: str                                   # 24-hour volume as decimal
    result: str                                          # Market result (e.g., "yes", "no")
    can_close_early: bool                                # Whether market can close before scheduled time
    open_interest: int                                   # Current open interest
    open_interest_fp: str                                # Open interest as decimal
    notional_value: int                                  # Notional value in cents
    notional_value_dollars: str                          # Notional value in dollars
    previous_yes_bid: int                                # Previous yes bid price in cents
    previous_yes_bid_dollars: str                        # Previous yes bid price in dollars
    previous_yes_ask: int                                # Previous yes ask price in cents
    previous_yes_ask_dollars: str                        # Previous yes ask price in dollars
    previous_price: int                                  # Previous price in cents
    previous_price_dollars: str                          # Previous price in dollars
    liquidity: int                                       # Market liquidity in cents
    liquidity_dollars: str                               # Market liquidity in dollars
    expiration_value: str                                # Value used for expiration calculation
    tick_size: int                                       # Minimum price increment
    rules_primary: str                                   # Primary market rules
    rules_secondary: str                                 # Secondary market rules
    price_level_structure: str                           # Description of price level structure
    price_ranges: list[PriceRange]                       # Available price ranges
    expected_expiration_time: str                        # ISO 8601 timestamp of expected expiration
    settlement_value: Optional[int] = None               # Settlement value in cents
    settlement_value_dollars: Optional[str] = None       # Settlement value in dollars
    settlement_ts: Optional[str] = None                  # ISO 8601 timestamp of settlement
    fee_waiver_expiration_time: Optional[str] = None     # ISO 8601 timestamp when fee waiver expires
    early_close_condition: Optional[str] = None          # Condition for early close
    strike_type: Optional[str] = None                    # Type of strike (e.g., "greater", "less")
    floor_strike: Optional[int] = None                   # Floor strike value
    cap_strike: Optional[int] = None                     # Cap strike value
    functional_strike: Optional[str] = None              # Functional strike description
    custom_strike: Optional[dict] = None                 # Custom strike configuration
    mve_collection_ticker: Optional[str] = None          # MVE collection identifier
    mve_selected_legs: Optional[list[MVESelectedLeg]] = None  # Selected legs for multi-variable events
    primary_participant_key: Optional[str] = None        # Primary participant identifier
    is_provisional: Optional[bool] = None               # Whether market is provisional


class MarketsResponse(BaseModel):
    markets: list[Market]                                # List of markets
    cursor: str                                          # Pagination cursor for next page


class Event(BaseModel):
    event_ticker: str                                        # Unique event identifier (e.g., "KXELONMARS-99")
    series_ticker: str                                       # Parent series identifier
    title: str                                               # Full title of the event
    sub_title: str                                           # Shortened descriptive title
    collateral_return_type: str                              # How collateral is returned (e.g., "binary")
    mutually_exclusive: bool                                 # If true, only one market can resolve "yes"
    category: str                                            # Event category (deprecated, use series-level)
    available_on_brokers: bool                               # Whether available to trade on brokers
    product_metadata: Optional[dict] = None                  # Additional metadata for the event
    strike_date: Optional[str] = None                        # Date strike (mutually exclusive with strike_period)
    strike_period: Optional[str] = None                      # Period strike e.g., "week", "month" (mutually exclusive with strike_date)
    markets: Optional[list[Market]] = None                   # Nested markets (only with with_nested_markets=true)


class Milestone(BaseModel):
    id: str                                                  # Unique identifier for the milestone
    category: str                                            # Category of the milestone
    type: str                                                # Type of the milestone
    start_date: str                                          # Start date of the milestone
    related_event_tickers: list[str]                         # Event tickers related to this milestone
    title: str                                               # Title of the milestone
    notification_message: str                                # Notification message for the milestone
    details: dict                                            # Additional details about the milestone
    primary_event_tickers: list[str]                         # Event tickers directly related to outcome
    last_updated_ts: str                                     # Last time this milestone was updated
    end_date: Optional[str] = None                           # End date of the milestone, if any
    source_id: Optional[str] = None                          # Source id of milestone if available


class EventResponse(BaseModel):
    event: Event                                             # Data for the event
    markets: list[Market]                                    # Markets in this event (deprecated, use event.markets with with_nested_markets=true)


class EventsResponse(BaseModel):
    cursor: str                                              # Pagination cursor for next page
    events: list[Event]                                      # List of events
    milestones: Optional[list[Milestone]] = None             # Associated milestones


class CandlestickOHLC(BaseModel):
    open: int                                                # Price at start of period (cents)
    open_dollars: str                                        # Price at start of period (dollars)
    low: int                                                 # Lowest price during period (cents)
    low_dollars: str                                         # Lowest price during period (dollars)
    high: int                                                # Highest price during period (cents)
    high_dollars: str                                        # Highest price during period (dollars)
    close: int                                               # Price at end of period (cents)
    close_dollars: str                                       # Price at end of period (dollars)


class CandlestickPriceOHLC(BaseModel):
    open: Optional[int] = None                               # First traded price during period (cents)
    open_dollars: Optional[str] = None                       # First traded price during period (dollars)
    low: Optional[int] = None                                # Lowest traded price during period (cents)
    low_dollars: Optional[str] = None                        # Lowest traded price during period (dollars)
    high: Optional[int] = None                               # Highest traded price during period (cents)
    high_dollars: Optional[str] = None                       # Highest traded price during period (dollars)
    close: Optional[int] = None                              # Last traded price during period (cents)
    close_dollars: Optional[str] = None                      # Last traded price during period (dollars)
    mean: Optional[int] = None                               # Mean traded price during period (cents)
    mean_dollars: Optional[str] = None                       # Mean traded price during period (dollars)
    previous: Optional[int] = None                           # Last traded price before period (cents)
    previous_dollars: Optional[str] = None                   # Last traded price before period (dollars)
    min: Optional[int] = None                                # Min close price of any market during period (cents)
    min_dollars: Optional[str] = None                        # Min close price of any market during period (dollars)
    max: Optional[int] = None                                # Max close price of any market during period (cents)
    max_dollars: Optional[str] = None                        # Max close price of any market during period (dollars)


class Candlestick(BaseModel):
    end_period_ts: int                                       # Unix timestamp for inclusive end of period
    yes_bid: CandlestickOHLC                                 # OHLC data for YES buy offers
    yes_ask: CandlestickOHLC                                 # OHLC data for YES sell offers
    price: CandlestickPriceOHLC                              # OHLC+ data for traded YES contract prices
    volume: int                                              # Contracts bought during period
    volume_fp: str                                           # Contracts bought during period (string)
    open_interest: int                                       # Contracts bought by end of period
    open_interest_fp: str                                    # Contracts bought by end of period (string)



class UnwrappedCandlestick(BaseModel):
    '''Flattened Candlestick — all nested OHLC fields prefixed by source for DataFrame use.'''
    end_period_ts: int                                       # Unix timestamp for inclusive end of period

    # --- YES BID OHLC ---
    yes_bid_open: int
    yes_bid_open_dollars: str
    yes_bid_low: int
    yes_bid_low_dollars: str
    yes_bid_high: int
    yes_bid_high_dollars: str
    yes_bid_close: int
    yes_bid_close_dollars: str

    # --- YES ASK OHLC ---
    # Ask being the prices that sellers want
    yes_ask_open: int
    yes_ask_open_dollars: str
    yes_ask_low: int
    yes_ask_low_dollars: str
    yes_ask_high: int
    yes_ask_high_dollars: str
    yes_ask_close: int
    yes_ask_close_dollars: str

    # --- PRICE OHLC (nullable — no trades in period) ---
    # Bid being the prices that buyers want
    price_open: Optional[int] = None
    price_open_dollars: Optional[str] = None
    price_low: Optional[int] = None
    price_low_dollars: Optional[str] = None
    price_high: Optional[int] = None
    price_high_dollars: Optional[str] = None
    price_close: Optional[int] = None
    price_close_dollars: Optional[str] = None
    price_mean: Optional[int] = None
    price_mean_dollars: Optional[str] = None
    price_previous: Optional[int] = None
    price_previous_dollars: Optional[str] = None
    price_min: Optional[int] = None
    price_min_dollars: Optional[str] = None
    price_max: Optional[int] = None
    price_max_dollars: Optional[str] = None

    # --- VOLUME / OPEN INTEREST ---
    volume: int                                              # Contracts bought during period
    volume_fp: str                                           # Contracts bought during period (string)
    open_interest: int                                       # Contracts bought by end of period
    open_interest_fp: str                                    # Contracts bought by end of period (string)



class EventCandlesticksResponse(BaseModel):
    market_tickers: list[str]                                # Market tickers in the event
    market_candlesticks: list[list[Candlestick]]             # Candlestick arrays, one per market
    adjusted_end_ts: int                                     # Adjusted end timestamp if request exceeded max


class TagList(BaseModel):
    tags: dict[str, Optional[list[str]]]  # Tags organized by category, None if no tags for that category

class MarketCandlestickResponse(BaseModel):
    ticker: str
    candlesticks: list[Candlestick]

