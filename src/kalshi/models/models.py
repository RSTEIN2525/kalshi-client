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

