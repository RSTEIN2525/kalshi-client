import requests
from .models import Series

class KalshiClient:

    API_KEY:str

    def __init__(self, API_KEY):
        self.API_KEY = API_KEY

    def get_series(self, series_name:str) -> Series:
        
        # Insert Series into Base URL Format
        url = f"https://api.elections.kalshi.com/trade-api/v2/series/{series_name}"

        # Call HTTP Endpoint, and Parse to JSON
        response = requests.get(url)
        series_data = response.json()

        series_data = series_data['series']  # Remove Outer Nesting
        
        # Create Series Data Model
        series = Series(
            ticker= series_data['ticker'],
            frequency= series_data['frequency'],
            title= series_data['title'],
            category= series_data['category'],
            tags= series_data['tags'],
            settlement_sources= series_data['settlement_sources'],
            contract_url= series_data['contract_url'],
            fee_type= series_data['fee_type'],
            fee_multiplier= series_data['fee_multiplier'],

            # .get() preferred below; optionally included, safe access required
            additional_prohibitions= series_data.get('additional_prohibitions'),
            product_metadata= series_data.get('product_metadata'),
            volume= series_data.get('volume'),
            volume_fp= series_data.get('volume_fp')
        )

        return series


      


