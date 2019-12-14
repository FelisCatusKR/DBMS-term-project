from datetime import datetime
from sqlalchemy import *
from sqlalchemy.orm import relationship
from app.database import Base


class Prescription(Base):
    __tablename__ = "prescriptions"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    hospital_reservation_id: int = Column(
        Integer, ForeignKey("hospital_reservations.id", ondelete="SET NULL")
    )
    hospital_reservation = relationship("HospReservation", uselist=False)
    filled_shop_id: int = Column(Integer, ForeignKey("shops.id", ondelete="SET NULL"))
    filled_date: datetime = Column(DateTime)
    filled_detail: str = Column(String)
    filled_drugs = relationship("PrescribedDrug")
