from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Time, Null
from database import Base


class Arrivals(Base):
    __tablename__ = "arrivals"

    id = Column(String, primary_key=True)
    iata_carrier_code = Column(String)
    flight_number = Column(Integer)
    sequence_number = Column(Integer)
    flight_type = Column(String)
    departure_airport = Column(String)
    departure_airport_icao = Column(String)
    departure_terminal = Column(String)
    departure_date = Column(Date)
    departure_time = Column(Time)
    arrival_airport = Column(String)
    arrival_airport_icao = Column(String)
    arrival_terminal = Column(String)
    arrival_date = Column(Date)
    arrival_time = Column(Time)
    aircraft_type = Column(String)
    number_of_stops = Column(Integer)
