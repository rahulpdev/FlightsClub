import requests


class DataManager:

    def __init__(self, uri, project, token):
        self.sheety_base_endpoint = "https://api.sheety.co"
        self.sheety_id = uri
        self.sheety_project = project
        self.sheety_token = token
        self.sheety_headers = {
            "Authorization": f"Bearer {self.sheety_token}",
            "Content-Type": "application/json",
        }

    def get_destinations_list(self, sheety_sheet):
        """Get list of all rows from Gsheet sheet"""
        sheety_endpoint = f"{self.sheety_base_endpoint}/{self.sheety_id}/{self.sheety_project}/{sheety_sheet}"
        response = requests.get(url=sheety_endpoint, headers=self.sheety_headers)
        response.raise_for_status()
        return response.json()[sheety_sheet]

    # Method for updating a column for all destinations
    def update_destinations_list(self, row, iata_code, sheety_sheet):
        """Put IATA code in all rows of Gsheet sheet"""
        sheety_params = {
            "price": {
                "iataCode": iata_code,
            }
        }
        sheety_endpoint = f"{self.sheety_base_endpoint}/{self.sheety_id}/{self.sheety_project}/{sheety_sheet}/{row}"
        response = requests.put(url=sheety_endpoint, headers=self.sheety_headers, json=sheety_params)
        response.raise_for_status()
