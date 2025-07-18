import logging
import yaml

from fastapi import Depends, FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response
from . import constants
from .logging import make_log_record
from .routers import router as api_router


logger = logging.getLogger(__name__)

app = FastAPI(title='Review API')
app.include_router(api_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.middleware('http')
async def handle_unhandled_exception(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception:
        logger.exception('Unhandled exception')
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content=jsonable_encoder({'detail': 'Unknown error'}))


@app.on_event('startup')
async def handle_startup_event():
    try:
        try:
            with open(constants.LOGGING_CONFIG_PATH, 'r') as file:
                logging_config = yaml.safe_load(file.read())
        except Exception as ex:
            raise Exception('Logging configuration loading failed') from ex
        logging.config.dictConfig(logging_config)
        logging.setLogRecordFactory(make_log_record)
        logger.info('Review API is starting...')
        try:
            from .config import config
        except Exception as ex:
            logger.exception('Review API configuration loading failed')
            raise Exception('Review API configuration loading failed') from ex
        from .db import create_db, ensure_session_factory_initialized
        await create_db()
        ensure_session_factory_initialized()
        logger.info('Review API is started')
    except Exception as ex:
        logger.exception('Review API starting failed')
        raise


@app.on_event('shutdown')
async def handle_shutdown_event():
    try:
        logger.info('Review API is stopping...')
        logger.info('Review API is stopped')
    except Exception as ex:
        logger.exception('Review API stopping failed')
        raise
