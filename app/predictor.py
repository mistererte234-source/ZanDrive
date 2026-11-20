from sqlalchemy.ext.asyncio import AsyncSession
from .crud import get_spot_stats
from datetime import datetime

async def recommend_spots(db: AsyncSession, user_id: int = None, limit: int = 5):
    now = datetime.utcnow()
    rows = await get_spot_stats(db, now.hour, now.weekday(), user_id=user_id, limit=limit)
    recs = []
    for row in rows:
        score = float(row.success_rate or 0) * min(row.samples, 20) / 20
        recs.append({
            "geohash": row.geohash,
            "lat": float(row.avg_lat),
            "lng": float(row.avg_lng),
            "score": round(score, 3),
            "sample_count": row.samples,
            "avg_success_rate": round(float(row.success_rate or 0), 3),
        })
    return recs
