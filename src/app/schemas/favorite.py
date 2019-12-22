from pydantic import *


class FavoriteHospital(BaseModel):
    user_id: int
    hospital_id: int

    class Config(BaseConfig):
        orm_mode = True


class FavoriteShop(BaseModel):
    user_id: int
    shop_id: int

    class Config(BaseConfig):
        orm_mode = True
