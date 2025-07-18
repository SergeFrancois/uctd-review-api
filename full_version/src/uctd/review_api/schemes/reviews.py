import datetime
from . import BaseModel
from ..models import Sentiment


class NewReview(BaseModel):
    text: str


class Review(BaseModel):
    id: int
    text: str
    sentiment: Sentiment
    created_at: datetime.datetime