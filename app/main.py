from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .database import engine, Base, get_db
from .schemas import LocationIn, SpotRecommendation
from .crud import create_log
from .predictor import recommend_spots
from typing import List

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

@app.get("/health")
async def health():
    return {"status": "ok"}
