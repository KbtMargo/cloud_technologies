from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database.base import Base

class DogPhoto(Base):
    __tablename__ = "dog_photos"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, nullable=False)
    breed = Column(String, nullable=False)
    sub_breed = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)  
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    stats = relationship("DogPhotoStats", back_populates="photo", uselist=False, lazy='selectin')


class DogPhotoStats(Base):
    __tablename__ = "dog_photo_stats"

    id = Column(Integer, primary_key=True, index=True)
    photo_id = Column(Integer, ForeignKey("dog_photos.id"), nullable=False)
    views = Column(Integer, default=0)
    last_viewed_at = Column(DateTime(timezone=True), nullable=True)
    
    photo = relationship("DogPhoto", back_populates="stats")