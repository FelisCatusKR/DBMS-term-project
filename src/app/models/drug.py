from sqlalchemy import *
from sqlalchemy.orm import relationship
from app.database import Base


class Drug(Base):
    __tablename__ = "drugs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True, index=True)
    unit = Column(String)
    prescribed_list = relationship("PrescribedDrug", back_populates="drug")


class PrescribedDrug(Base):
    __tablename__ = "prescribed_drugs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    drug_id = Column(Integer, ForeignKey("drugs.id", ondelete="SET NULL"))
    drug = relationship("Drug", uselist=False, back_populates="prescribed_list")
    prescription_id = Column(
        Integer, ForeignKey("prescriptions.id", ondelete="SET NULL")
    )
    drug_amount_per_taking = Column(Integer, nullable=False)
    drug_doses_per_day = Column(Integer, nullable=False)
    drug_total_days = Column(Integer, nullable=False)
