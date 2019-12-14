from sqlalchemy import *
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from app.database import Base


class Shop(Base):
    __tablename__ = "shops"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    addr = Column(String, nullable=False)
    lon = Column(Float, nullable=False)
    lat = Column(Float, nullable=False)
    tel = Column(String, nullable=False)
    geom = Column(Geometry("POINT"), nullable=False)
    is_pharmacy = Column(Boolean, nullable=False, index=True)
    dutyTime1s = Column(Time)
    dutyTime1c = Column(Time)
    dutyTime2s = Column(Time)
    dutyTime2c = Column(Time)
    dutyTime3s = Column(Time)
    dutyTime3c = Column(Time)
    dutyTime4s = Column(Time)
    dutyTime4c = Column(Time)
    dutyTime5s = Column(Time)
    dutyTime5c = Column(Time)
    dutyTime6s = Column(Time)
    dutyTime6c = Column(Time)
    dutyTime7s = Column(Time)
    dutyTime7c = Column(Time)
    dutyTime8s = Column(Time)
    dutyTime8c = Column(Time)
    admins = relationship("User")
    reservations = relationship("ShopReservation")
