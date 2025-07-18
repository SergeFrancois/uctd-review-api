import datetime
import logging
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy import select
from ..db import AsyncSession, models as db_models
from ..models import Sentiment
from ..schemes.reviews import NewReview, Review
from ..utils import get_sentiment_by_review_text


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/reviews',
    tags=['Reviews']
)


@router.post('/', response_model=Review, response_model_by_alias=False)
async def add_review(review: NewReview, response: Response):
    async with AsyncSession.begin() as session:
        db_review = db_models.Review(
            text=review.text,
            sentiment=get_sentiment_by_review_text(review.text),
            created_at=datetime.datetime.utcnow()
        )
        session.add(db_review)
    result_review = Review.model_validate(db_review, from_attributes=True)
    response.status_code = status.HTTP_201_CREATED
    logger.info(f'New review is added: {result_review!r}')
    return result_review


@router.get('/', response_model=list[Review], response_model_by_alias=False)
async def get_reviews(sentiment: Sentiment | None = None):
    query = select(db_models.Review).order_by(db_models.Review.id)
    if sentiment:
        query = query.where(db_models.Review.sentiment == sentiment)
    async with AsyncSession.begin() as session:
        reviews = (await session.execute(query)).unique().scalars().all()
    return [
        Review.model_validate(r, from_attributes=True)
        for r in reviews
    ]