import asyncio
import datetime
import sqlite3
from enum import StrEnum
from fastapi import Depends, FastAPI, status
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response


DB_URL = 'reviews.sqlite'

app = FastAPI(title='Review API')
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


class Sentiment(StrEnum):
    NEGATIVE = 'negative'
    NEUTRAL = 'neutral'
    POSITIVE = 'positive'


class NewReview(BaseModel):
    text: str


class Review(BaseModel):
    id: int
    text: str
    sentiment: Sentiment
    created_at: datetime.datetime


def row_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


def get_db_connection():
    connection = sqlite3.connect(DB_URL, check_same_thread=False)
    connection.row_factory = row_factory
    try:
        yield connection
    finally:
        connection.close()


def get_sentiment_by_review_text(text):
    if any(k in text for k in ('хорош', 'люблю')):
        return Sentiment.POSITIVE
    if any(k in text for k in ('плохо', 'ненавиж')):
        return Sentiment.NEGATIVE
    return Sentiment.NEUTRAL


@app.on_event('startup')
async def handle_startup_event():
    sqlite3.register_adapter(
        datetime.datetime,
        lambda value: value.replace(tzinfo=None).isoformat()
    )
    sqlite3.register_converter(
        'datetime',
        lambda value: datetime.datetime.fromisoformat(value.decode())
    )
    sql = (
        'create table if not exists reviews ('
            'id integer primary key autoincrement, '
            'text text not null, '
            'sentiment text not null, '
            'created_at text not null'
        ');'
    )
    loop = asyncio.get_running_loop()
    connection = sqlite3.connect(DB_URL, check_same_thread=False)
    try:
        with connection:
            await loop.run_in_executor(None, lambda: connection.execute(sql))
    finally:
        connection.close()


@app.post('/api/reviews/', response_model=Review, response_model_by_alias=False)
async def add_review(review: NewReview, response: Response, db_connection=Depends(get_db_connection)):
    loop = asyncio.get_running_loop()
    with db_connection:
        cursor = db_connection.cursor()
        await loop.run_in_executor(
            None,
            cursor.execute,
            'insert into reviews '
            '(text, sentiment, created_at) '
            'values (?, ?, ?) '
            'returning *',
            (
                review.text,
                get_sentiment_by_review_text(review.text),
                datetime.datetime.utcnow()
            )
        )
        result = await loop.run_in_executor(None, cursor.fetchone)
    result_review = Review.model_validate(result, from_attributes=True)
    response.status_code = status.HTTP_201_CREATED
    return result_review


@app.get('/api/reviews/', response_model=list[Review], response_model_by_alias=False)
async def get_reviews(sentiment: Sentiment | None = None, db_connection=Depends(get_db_connection)):
    loop = asyncio.get_running_loop()
    with db_connection:
        cursor = db_connection.cursor()
        await loop.run_in_executor(
            None,
            cursor.execute,
            'select * from reviews{where_condition}'.format(
                where_condition=' where sentiment=?' if sentiment else ''
            ),
            (sentiment,) if sentiment else ()
        )
        reviews = await loop.run_in_executor(None, cursor.fetchall)
    return [
        Review.model_validate(r, from_attributes=True)
        for r in reviews
    ]