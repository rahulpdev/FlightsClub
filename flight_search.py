import requests


class FlightSearch:

    def __init__(self, api_key, currency, home_code):
        self.home_currency = currency
        self.home_iata_code = home_code
        self.base_endpoint = "https://api.tequila.kiwi.com"
        self.flight_search_api_key = api_key
        self.headers = {
            "apikey": self.flight_search_api_key,
        }

    def flights_search(self, destination_code, max_price, start_date, end_date, min_nights=7, max_nights=28):
        """Get list from Tequila of available flights under the max price and within time window"""
        search_endpoint = f"{self.base_endpoint}/v2/search"
        search_params = {
            "flight_type": "round",
            "fly_from": f'city:{self.home_iata_code}',
            "fly_to": f'city:{destination_code}',
            "date_from": start_date,
            "date_to": end_date,
            "nights_in_dst_from": min_nights,
            "nights_in_dst_to": max_nights,
            "price_to": int(max_price),
            "curr": self.home_currency,
        }
        response = requests.get(url=search_endpoint, headers=self.headers, params=search_params)
        response.raise_for_status()
        return response.json()["data"]

    def iata_code_search(self, city):
        """Get list from Tequila of IATA code for a city"""
        locations_endpoint = f"{self.base_endpoint}/locations/query"
        locations_params = {
            "term": city,
            "location_types": "city",
        }
        response = requests.get(url=locations_endpoint, headers=self.headers, params=locations_params)
        response.raise_for_status()
        return response.json()["locations"][0]["code"]
