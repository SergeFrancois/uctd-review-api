from sqlalchemy import DateTime, Integer, String
from sqlalchemy.dialects.sqlite import DATETIME, INTEGER, TEXT
from sqlalchemy.orm import DeclarativeBase, mapped_column


ISO_DATETIME = DATETIME(
    storage_format='%(year)04d-%(month)02d-%(day)02dT%(hour)02d:%(minute)02d:%(second)02d.%(microsecond)06d',
    regexp=r'(\d+)-(\d+)-(\d+)T(\d+):(\d+):(\d+)(?:\.(\d+))?',
)


class BaseModel(DeclarativeBase):
    pass


class Review(BaseModel):
    
    __tablename__ = 'reviews'
    
    id = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    text = mapped_column(TEXT, nullable=False)
    sentiment = mapped_column(TEXT, nullable=False)
    created_at = mapped_column(ISO_DATETIME, nullable=False)
