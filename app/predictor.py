from sqlalchemy.ext.asyncio import AsyncSession
from .crud import get_spot_stats
from datetime import datetime

async def recommend_spots(db: AsyncSession, limit: int = 5):
    now = datetime.utcnow()
    rows = await get_spot_stats(db, now.hour, now.weekday(), limit=limit)
    recs = []
    for row in rows:
        score = float(row.success_rate or 0) * min(row.samples, 20) / 20
        recs.append({
            "geohash": row.geohash,
            "lat": row.avg_lat,
            "lng": row.avg_lng,
            "score": round(score, 3),
            "sample_count": row.samples,
            "avg_success_rate": round(float(row.success_rate or 0), 3),
        })
    return recs
