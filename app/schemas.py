from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str

class UserOut(BaseModel):
    id: int
    username: str
    api_key: str

    class Config:
        from_attributes = True

class LocationIn(BaseModel):
    lat: float
    lng: float
    status: str = "idle"
    got_passenger: bool = False
    wait_minutes: Optional[int] = None

class SpotRecommendation(BaseModel):
    geohash: str
    lat: float
    lng: float
    score: float
    sample_count: int
    avg_success_rate: float
