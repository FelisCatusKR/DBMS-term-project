from sqlalchemy import *
from app.database import Base


class FavoriteHospital(Base):
    __tablename__ = "favorite_hospitals"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id", ondelete="CASCADE"), primary_key=True)


class FavoriteShop(Base):
    __tablename__ = "favorites_shops"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    shop_id = Column(Integer, ForeignKey("shops.id", ondelete="CASCADE"), primary_key=True)
