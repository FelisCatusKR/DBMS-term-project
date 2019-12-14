from sqlalchemy import *
from app.database import Base


class Drug(Base):
    __tablename__ = "drugs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True, index=True)
    unit = Column(String)
