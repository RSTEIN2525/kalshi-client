from kalshi import KalshiClient, Series
from utils import pydantic_model_to_dataframe
from dotenv import load_dotenv
import os

def main():

    # Pull Kalshi API Key from ENV
    load_dotenv() # Load Environment File
    KALSHI_API_KEY = os.getenv("KALSHI_API_KEY")

    # Validate Key
    if not KALSHI_API_KEY:
        raise ValueError("missing 'KALSHI_API_KEY' in .env")

    # init Client
    kc = KalshiClient(KALSHI_API_KEY)

    # Pull Series
    series_data: Series = kc.get_series("KXHIGHNY")

    # Pull Markets
    markets = kc.get_open_markets_general(limit=1)

    # Convert to DF
    formatted_markets = pydantic_model_to_dataframe(markets.markets)
    print(formatted_markets)
    


if __name__ == '__main__':
    main()