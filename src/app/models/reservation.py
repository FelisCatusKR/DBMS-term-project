from sqlalchemy import *
from sqlalchemy.orm import relationship
from app.database import Base


class HospReservation(Base):
    __tablename__ = "hospital_reservations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    hosp_id = Column(Integer, ForeignKey("hospitals.id", ondelete="SET NULL"))
    date = Column(DateTime, nullable=False)


class ShopReservation(Base):
    __tablename__ = "shop_reservations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    shop_id = Column(Integer, ForeignKey("shops.id", ondelete="SET NULL"))
    date = Column(DateTime, nullable=False)
    prescription_id = Column(
        Integer, ForeignKey("prescriptions.id", ondelete="SET NULL")
    )
    prescription = relationship("Prescription", uselist=False)
    is_able_to_prescribe = Column(Boolean)
