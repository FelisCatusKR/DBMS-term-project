from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import relationship

from app.database import Base


class PrescribedDrug(Base):
    __tablename__ = "prescribed_drugs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    drug_id = Column(Integer, ForeignKey("drugs.id", ondelete="SET NULL"))
    drug = relationship("Drug", uselist=False)
    drug_amount_per_dose = Column(Integer, nullable=False)
    drug_doses_per_day = Column(Integer, nullable=False)
    drug_total_days = Column(Integer, nullable=False)
    prescription_id = Column(
        Integer, ForeignKey("prescriptions.id", ondelete="SET NULL")
    )


class Prescription(Base):
    __tablename__ = "prescriptions"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    hospital_reservation_id: int = Column(
        Integer, ForeignKey("hospital_reservations.id", ondelete="SET NULL")
    )
    hospital_reservation = relationship("HospReservation", uselist=False)
    prescribed_date: datetime = Column(DateTime)
    prescribed_drugs = relationship("PrescribedDrug")
    filled_shop_id: int = Column(Integer, ForeignKey("shops.id", ondelete="SET NULL"))
    filled_date: datetime = Column(DateTime)
    filled_detail: str = Column(String)
