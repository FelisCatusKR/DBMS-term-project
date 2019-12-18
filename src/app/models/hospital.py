from datetime import time
from sqlalchemy import *
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from app.database import Base


class Hospital(Base):
    __tablename__ = "hospitals"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String, nullable=False)
    addr: str = Column(String, nullable=False)
    tel: str = Column(String, nullable=False)
    lon: float = Column(Float, nullable=False)
    lat: float = Column(Float, nullable=False)
    geom: str = Column(Geometry("POINT", srid=4326), nullable=False)
    strCnd: int = Column(Integer, nullable=False)
    dutyTime1s: time = Column(Time)
    dutyTime1c: time = Column(Time)
    dutyTime2s: time = Column(Time)
    dutyTime2c: time = Column(Time)
    dutyTime3s: time = Column(Time)
    dutyTime3c: time = Column(Time)
    dutyTime4s: time = Column(Time)
    dutyTime4c: time = Column(Time)
    dutyTime5s: time = Column(Time)
    dutyTime5c: time = Column(Time)
    dutyTime6s: time = Column(Time)
    dutyTime6c: time = Column(Time)
    dutyTime7s: time = Column(Time)
    dutyTime7c: time = Column(Time)
    dutyTime8s: time = Column(Time)
    dutyTime8c: time = Column(Time)
    course_bitmask: int = Column(Integer, nullable=False)
    doctors = relationship("User")
    reservations = relationship("HospReservation")
