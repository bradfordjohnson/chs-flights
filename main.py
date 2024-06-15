from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from uuid import uuid4


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
