from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from .models import LocationLog, User
from .schemas import LocationIn, UserCreate
import geohash2
from datetime import datetime
import secrets

async def create_user(db: AsyncSession, data: UserCreate):
    api_key = secrets.token_urlsafe(32)
    user = User(username=data.username, api_key=api_key)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_user_by_key(db: AsyncSession, api_key: str):
    result = await db.execute(select(User).where(User.api_key == api_key))
    return result.scalar_one_or_none()

async def create_log(db: AsyncSession, user_id: int, data: LocationIn):
    now = datetime.utcnow()
    gh = geohash2.encode(data.lat, data.lng, precision=6)
    log = LocationLog(
        user_id=user_id,
        lat=data.lat,
        lng=data.lng,
        geohash=gh,
        hour=now.hour,
        day_of_week=now.weekday(),
        status=data.status,
        got_passenger=data.got_passenger,
        wait_minutes=data.wait_minutes,
    )
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return log

async def get_spot_stats(db: AsyncSession, hour: int, day_of_week: int, user_id: int = None, limit: int = 10):
    stmt = (
        select(
            LocationLog.geohash,
            func.avg(LocationLog.lat).label("avg_lat"),
            func.avg(LocationLog.lng).label("avg_lng"),
            func.count().label("samples"),
            func.avg(LocationLog.got_passenger.cast(Integer)).label("success_rate"),
        )
        .where(LocationLog.hour == hour)
        .where(LocationLog.day_of_week == day_of_week)
    )
    if user_id:
        stmt = stmt.where(LocationLog.user_id == user_id)
    stmt = (
        stmt.group_by(LocationLog.geohash)
        .having(func.count() >= 2)
        .order_by(func.avg(LocationLog.got_passenger.cast(Integer)).desc())
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.all()
