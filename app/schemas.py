from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LocationIn(BaseModel):
    user_id: str
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
