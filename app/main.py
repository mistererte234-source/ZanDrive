from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .database import engine, Base, get_db
from .schemas import LocationIn, SpotRecommendation
from .crud import create_log
from .predictor import recommend_spots
from typing import List
import random

app = FastAPI(title="ZanDrive", version="0.1.0")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/log", response_model=dict)
async def log_location(data: LocationIn, db: AsyncSession = Depends(get_db)):
    log = await create_log(db, data)
    return {"id": log.id, "geohash": log.geohash, "status": "logged"}

@app.get("/recommend", response_model=List[SpotRecommendation])
async def get_recommendations(db: AsyncSession = Depends(get_db)):
    return await recommend_spots(db)

@app.post("/seed")
async def seed_dummy_data(db: AsyncSession = Depends(get_db)):
    """Generate sample data around Surabaya for testing."""
    base_spots = [
        (-7.2575, 112.7521),  # Surabaya center
        (-7.2650, 112.7450),
        (-7.2500, 112.7600),
        (-7.2700, 112.7400),
        (-7.2450, 112.7550),
    ]
    count = 0
    for _ in range(80):
        lat, lng = random.choice(base_spots)
        lat += random.uniform(-0.01, 0.01)
        lng += random.uniform(-0.01, 0.01)
        got = random.random() < 0.65
        data = LocationIn(
            user_id=f"driver{random.randint(1,5)}",
            lat=lat,
            lng=lng,
            status="waiting",
            got_passenger=got,
            wait_minutes=random.randint(2, 25) if not got else random.randint(1, 12),
        )
        await create_log(db, data)
        count += 1
    return {"seeded": count}

@app.get("/health")
async def health():
    return {"status": "ok"}
