import json
import requests


def get_url(key: str, path: str = "./config.json"):
    with open(path) as f:
        return json.load(f).get(key)


def get_flights(key):
    response = requests.get(key)
    flights = response.json()
    return flights["data"]


def noramlize_flights(flights_list: list):
    normalized_flights = []
    for flight in flights_list:
        individual_flight = {
            "iata_carrier_code": flight["carrierCode"]["iata"],
            "flight_number": flight["flightNumber"],
            "sequence_number": flight["sequenceNumber"],
            "flight_type": flight["flightType"],
            "departure_airport": flight["departure"]["airport"]["iata"],
            "departure_airport_icao": flight["departure"]["airport"]["icao"],
            "departure_terminal": flight["departure"]["terminal"],
            "departure_date": flight["departure"]["date"],
            "departure_time": flight["departure"]["passengerLocalTime"],
            "arrival_airport": flight["arrival"]["airport"]["iata"],
            "arrival_airport_icao": flight["arrival"]["airport"]["icao"],
            "arrival_terminal": flight["arrival"]["terminal"],
            "arrival_date": flight["arrival"]["date"],
            "arrival_time": flight["arrival"]["passengerLocalTime"],
            "aircraft_type": flight["aircraftType"]["iata"],
            "number_of_stops": flight["segmentInfo"]["numberOfStops"],
        }

        normalized_flights.append(individual_flight)

        return normalized_flights


def main():
    arrivals = noramlize_flights(get_flights(get_url(key="ARRIVALS_URL")))
    print(arrivals[0])

    departures = noramlize_flights(get_flights(get_url(key="DEPARTURES_URL")))
    print(departures[0])


if __name__ == "__main__":
    main()
