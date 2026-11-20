from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Index
from sqlalchemy.sql import func
from .database import Base

class LocationLog(Base):
    __tablename__ = "location_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    geohash = Column(String(12), index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    hour = Column(Integer, index=True)
    day_of_week = Column(Integer, index=True)  # 0=Monday
    status = Column(String)  # idle, waiting, on_trip
    got_passenger = Column(Boolean, default=False)
    wait_minutes = Column(Integer, nullable=True)

    __table_args__ = (
        Index('ix_geohash_hour_dow', 'geohash', 'hour', 'day_of_week'),
    )
