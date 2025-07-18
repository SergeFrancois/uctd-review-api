from fastapi import APIRouter
from . import reviews


router = APIRouter(prefix='/api')
router.include_router(reviews.router)