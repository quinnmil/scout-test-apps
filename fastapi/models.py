from pydantic import BaseModel
from database import Base


class User(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool

    class Config:
        orm_mode = True
