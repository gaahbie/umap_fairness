from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    experiment_id: str
    experiment_type: int
    email: Optional[str]

class InteractionCreate(BaseModel):
    item_id: str
    rating: int
    user_id: str

class AddPopularity(BaseModel):
    experiment_id: str
    H: float
    M: float
    T: float

