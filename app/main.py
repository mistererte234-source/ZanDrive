from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from .database import engine, Base, get_db
from .schemas import LocationIn, SpotRecommendation, UserCreate, UserOut
from .crud import create_log, create_user, get_user_by_key
from .predictor import recommend_spots
from typing import List, Optional

app = FastAPI(title="ZanDrive", version="0.2.0")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_current_user(x_api_key: str = Header(...), db: AsyncSession = Depends(get_db)):
    user = await get_user_by_key(db, x_api_key)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return user

@app.post("/register", response_model=UserOut)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db, data)

@app.post("/log")
async def log_location(
    data: LocationIn,
    user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    log = await create_log(db, user.id, data)
    return {"id": log.id, "geohash": log.geohash, "status": "logged"}

@app.get("/recommend", response_model=List[SpotRecommendation])
async def get_recommendations(
    personal: bool = True,
    user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    uid = user.id if personal else None
    return await recommend_spots(db, user_id=uid)

@app.get("/health")
async def health():
    return {"status": "ok"}
