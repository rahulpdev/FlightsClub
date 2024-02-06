import os
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager

# Define personal variables
home_currency = "GBP"
home_city = "London"
home_iata_code = "LON"
flights_search_window = 182
min_num_of_nights = 7
max_num_of_nights = 28
sheety_prices_sheet = "prices"

# Define environment variables
sheety_id = os.environ["SHEETY_PROJECT_URI"]
sheety_project = os.environ["SHEETY_PROJECT_NAME"]
sheety_token = os.environ["SHEETY_TOKEN"]
flight_search_api_key = os.environ["FLIGHT_SEARCH_API_KEY"]
twilio_account_sid = os.environ["TWILIO_ACCOUNT_SID"]
twilio_auth_token = os.environ["TWILIO_AUTH_TOKEN"]
twilio_phone = os.environ["TWILIO_PHONE"]
my_phone = os.environ["MY_PHONE"]

# Define program variables
flights_search_start_date = datetime.today() + timedelta(days=1)
flights_search_end_date = datetime.today() + timedelta(days=flights_search_window)

# Get list from Gsheet of flight destination cities
data_manager = DataManager(
    sheety_id, sheety_project, sheety_token
)
destination_list = data_manager.get_destinations_list(sheety_prices_sheet)

# Get IATA code from Tequila for each flight destination city and put in Gsheet
flight_search = FlightSearch(
    flight_search_api_key, home_currency, home_iata_code
)
destination_sheet_row = 2
for city in destination_list:
    city_iata_code = flight_search.iata_code_search(city["city"])
    data_manager.update_destinations_list(destination_sheet_row, city_iata_code, sheety_prices_sheet)
    destination_sheet_row += 1

# Get list from Gsheet of flight destination cities
destination_list = data_manager.get_destinations_list(sheety_prices_sheet)

for destination in destination_list:
    # Get list from Tequila of available flights under the max price and within search window
    cheap_flights_list = flight_search.flights_search(
        destination["iataCode"], int(destination["lowestPrice"]), flights_search_start_date.strftime("%d/%m/%Y"), flights_search_end_date.strftime("%d/%m/%Y"), min_num_of_nights, max_num_of_nights
    )
    if len(cheap_flights_list) > 0:
        # Find the lowest priced flight in the list
        flight_data = FlightData(
            destination["city"], int(destination["lowestPrice"])
        )
        flight_data.find_cheapest_flight(cheap_flights_list)

        # Send SMS with relevant details of cheapest flight
        notification_manager = NotificationManager(
            twilio_account_sid, twilio_auth_token, twilio_phone, my_phone
        )
        notification_manager.send_flight_deals(
            f'Low price flight alert! Only {home_currency}{flight_data.lowest_price} from {home_city}-{flight_data.depart_airport} to {destination["city"]}-{flight_data.arrive_airport}, from {flight_data.depart_local_time.split("T")[0]} to {flight_data.arrive_local_time.split("T")[0]}'
        )
