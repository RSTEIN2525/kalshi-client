from pydantic import BaseModel
from typing import Optional

class Series(BaseModel):
    ticker: str                                          # Unique identifier (e.g., "KXHIGHNY", "INX")
    frequency: str                                       # How often events occur ("daily", "weekly", "monthly")
    title: str                                           # Human-readable name
    category: str                                        # Market category (e.g., "Economics", "Weather", "Politics")
    tags: list[str]                                      # Keywords for filtering/search
    settlement_sources: list[dict[str, str]]             # Where official data comes from to settle markets
    contract_url: str                                    # Link to contract details
    fee_type: str                                        # Fee structure type (typically "quadratic")
    fee_multiplier: int                                  # Multiplier for fee calculation
    additional_prohibitions: Optional[list[str]] = None  # Extra trading restrictions
    product_metadata: Optional[dict] = None              # Custom metadata specific to this series
    volume: Optional[int] = None                         # Total trading volume (in cents)
    volume_fp: Optional[str] = None                      # Trading volume as decimal (in dollars)


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
    strike_type: str                                     # Type of strike (e.g., "greater", "less")
    floor_strike: Optional[int] = None                   # Floor strike value
    cap_strike: Optional[int] = None                     # Cap strike value
    functional_strike: Optional[str] = None              # Functional strike description
    custom_strike: dict                                  # Custom strike configuration
    mve_collection_ticker: str                           # MVE collection identifier
    mve_selected_legs: list[MVESelectedLeg]              # Selected legs for multi-variable events
    primary_participant_key: Optional[str] = None        # Primary participant identifier
    is_provisional: bool                                 # Whether market is provisional


class MarketsResponse(BaseModel):
    markets: list[Market]                                # List of markets
    cursor: str                                          # Pagination cursor for next page

