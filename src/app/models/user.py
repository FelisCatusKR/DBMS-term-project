from sqlalchemy import *
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from app.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    tel = Column(String, nullable=False, index=True)
    lon = Column(Float, nullable=False)
    lat = Column(Float, nullable=False)
    geom = Column(Geometry("Point"), nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    hosp_id = Column(Integer, ForeignKey("hospitals.id", ondelete="SET NULL"))
    shop_id = Column(Integer, ForeignKey("shops.id", ondelete="SET NULL"))
    hospital_reservations = relationship("HospReservation")
    shop_reservations = relationship("ShopReservation")
