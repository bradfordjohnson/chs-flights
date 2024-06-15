# chs-flights

This is a full stack web app I'm developing locally to interact with flight data.

## Tech Stack

- FastAPI
- React?
- PostgreSQL

## Random code to put into a script soon

```python
import json
import requests
from uuid import uuid4

with open('config.json') as f:
    ARRIVALS_URL = json.load(f).get('ARRIVALS_URL')
    
response = requests.get(ARRIVALS_URL)

raw_flights = response.json()

flights_response_entry = raw_flights['data']

flat_flights = []
for flight in flights_response_entry:
    flattened_flight = {
        id = uuid4(),
        'iata_carrier_code': flight['carrierCode']['iata'],
        'flight_number': flight['flightNumber'],
        'sequence_number': flight['sequenceNumber'],
        'flight_type': flight['flightType'],
        'departure_airport': flight['departure']['airport']['iata'],
        'departure_airport_icao': flight['departure']['airport']['icao'],
        'departure_terminal': flight['departure']['terminal'],
        'departure_date': flight['departure']['date'],
        'departure_time': flight['departure']['passengerLocalTime'],
        'arrival_airport': flight['arrival']['airport']['iata'],
        'arrival_airport_icao': flight['arrival']['airport']['icao'],
        'arrival_terminal': flight['arrival']['terminal'],
        'arrival_date': flight['arrival']['date'],
        'arrival_time': flight['arrival']['passengerLocalTime'],
        'aircraft_type': flight['aircraftType']['iata'],
        'number_of_stops': flight['segmentInfo']['numberOfStops']
    }
    
    flat_flights.append(flattened_flight)
    
print(flat_flights)
```
