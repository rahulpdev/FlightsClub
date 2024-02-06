class FlightData:

    def __init__(self, destination, max_price):
        self.destination_city = destination
        self.lowest_price = max_price
        self.depart_airport = ""
        self.arrive_airport = ""
        self.depart_local_time = ""
        self.arrive_local_time = ""

    def find_cheapest_flight(self, cheap_flights_list):
        """Find the lowest priced flight in a list of flights returned from Tequila"""
        for flight in cheap_flights_list:
            if flight["price"] < self.lowest_price:
                self.lowest_price = flight["price"]
                self.depart_airport = flight["flyFrom"]
                self.arrive_airport = flight["flyTo"]
                self.depart_local_time = flight["local_departure"]
                self.arrive_local_time = flight["local_arrival"]
