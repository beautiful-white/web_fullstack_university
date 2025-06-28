from pydantic import BaseModel


class TableBase(BaseModel):
    seats: int
    is_available: bool = True


class TableCreate(TableBase):
    restaurant_id: int


class TableRead(TableBase):
    id: int
    restaurant_id: int

    class Config:
        orm_mode = True
