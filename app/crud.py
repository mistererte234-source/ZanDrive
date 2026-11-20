from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from .models import LocationLog
from .schemas import LocationIn
import geohash2
from datetime import datetime

async def create_log(db: AsyncSession, data: LocationIn):
    now = datetime.utcnow()
    gh = geohash2.encode(data.lat, data.lng, precision=6)
    log = LocationLog(
        user_id=data.user_id,
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

async def get_spot_stats(db: AsyncSession, hour: int, day_of_week: int, limit: int = 10):
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
        .group_by(LocationLog.geohash)
        .having(func.count() >= 3)
        .order_by(func.avg(LocationLog.got_passenger.cast(Integer)).desc())
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.all()
