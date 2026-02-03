from kalshi import KalshiClient, Series
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
    
    print(series_data.category)


if __name__ == '__main__':
    main()