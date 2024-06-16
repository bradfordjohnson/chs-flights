from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from uuid import uuid4
from etl.batch_flights import normalize_flights, get_flights, get_url

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


class ArrivalBase(BaseModel):
    iata_carrier_code: str
    flight_number: int
    sequence_number: int
    flight_type: str
    departure_airport: str
    departure_airport_icao: str
    departure_terminal: str
    departure_date: str
    departure_time: str
    arrival_airport: str
    arrival_airport_icao: str
    arrival_terminal: str
    arrival_date: str
    arrival_time: str
    aircraft_type: str
    number_of_stops: int


class DepartureBase(BaseModel):
    iata_carrier_code: str
    flight_number: int
    sequence_number: int
    flight_type: str
    departure_airport: str
    departure_airport_icao: str
    departure_terminal: str
    departure_date: str
    departure_time: str
    arrival_airport: str
    arrival_airport_icao: str
    arrival_terminal: str
    arrival_date: str
    arrival_time: str
    aircraft_type: str
    number_of_stops: int


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.post("/arrivals/")
async def add_flight(arrival: ArrivalBase, db: db_dependency):
    db_arrivals = models.Arrivals(
        iata_carrier_code=arrival.iata_carrier_code,
        flight_number=arrival.flight_number,
        sequence_number=arrival.sequence_number,
        flight_type=arrival.flight_type,
        departure_airport=arrival.departure_airport,
        departure_airport_icao=arrival.departure_airport_icao,
        departure_terminal=arrival.departure_terminal,
        departure_date=arrival.departure_date,
        departure_time=arrival.departure_time,
        arrival_airport=arrival.arrival_airport,
        arrival_airport_icao=arrival.arrival_airport_icao,
        arrival_terminal=arrival.arrival_terminal,
        arrival_date=arrival.arrival_date,
        arrival_time=arrival.arrival_time,
        aircraft_type=arrival.aircraft_type,
        number_of_stops=arrival.number_of_stops,
        id=uuid4(),
    )
    db.add(db_arrivals)
    db.commit()


@app.post("/departures/")
async def add_flight(departure: DepartureBase, db: db_dependency):
    db_departures = models.Arrivals(
        iata_carrier_code=departure.iata_carrier_code,
        flight_number=departure.flight_number,
        sequence_number=departure.sequence_number,
        flight_type=departure.flight_type,
        departure_airport=departure.departure_airport,
        departure_airport_icao=departure.departure_airport_icao,
        departure_terminal=departure.departure_terminal,
        departure_date=departure.departure_date,
        departure_time=departure.departure_time,
        arrival_airport=departure.arrival_airport,
        arrival_airport_icao=departure.arrival_airport_icao,
        arrival_terminal=departure.arrival_terminal,
        arrival_date=departure.arrival_date,
        arrival_time=departure.arrival_time,
        aircraft_type=departure.aircraft_type,
        number_of_stops=departure.number_of_stops,
        id=uuid4(),
    )
    db.add(db_departures)
    db.commit()


@app.get("/bulk/flights/etl/")
async def bulk_add_flights(db: Session = Depends(get_db)):
    try:
        arrivals = normalize_flights(get_flights(get_url(key="ARRIVALS_URL")))
        for arrival in arrivals:
            db_arrivals = models.Arrivals(
                iata_carrier_code=arrival["iata_carrier_code"],
                flight_number=arrival["flight_number"],
                sequence_number=arrival["sequence_number"],
                flight_type=arrival["flight_type"],
                departure_airport=arrival["departure_airport"],
                departure_airport_icao=arrival["departure_airport_icao"],
                departure_terminal=arrival["departure_terminal"],
                departure_date=arrival["departure_date"],
                departure_time=arrival["departure_time"],
                arrival_airport=arrival["arrival_airport"],
                arrival_airport_icao=arrival["arrival_airport_icao"],
                arrival_terminal=arrival["arrival_terminal"],
                arrival_date=arrival["arrival_date"],
                arrival_time=arrival["arrival_time"],
                aircraft_type=arrival["aircraft_type"],
                number_of_stops=arrival["number_of_stops"],
                id=uuid4(),
            )
            db.add(db_arrivals)
        db.commit()

        departures = normalize_flights(get_flights(get_url(key="DEPARTURES_URL")))
        for departure in departures:
            db_departures = models.Departures(
                iata_carrier_code=departure["iata_carrier_code"],
                flight_number=departure["flight_number"],
                sequence_number=departure["sequence_number"],
                flight_type=departure["flight_type"],
                departure_airport=departure["departure_airport"],
                departure_airport_icao=departure["departure_airport_icao"],
                departure_terminal=arrival["departure_terminal"],
                departure_date=departure["departure_date"],
                departure_time=departure["departure_time"],
                arrival_airport=departure["arrival_airport"],
                arrival_airport_icao=departure["arrival_airport_icao"],
                arrival_terminal=departure["arrival_terminal"],
                arrival_date=departure["arrival_date"],
                arrival_time=departure["arrival_time"],
                aircraft_type=departure["aircraft_type"],
                number_of_stops=departure["number_of_stops"],
                id=uuid4(),
            )
            db.add(db_departures)
        db.commit()

        return {"status": "success", "message": "Flights added successfully"}

    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}
