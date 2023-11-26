from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from loguru import logger
from north_admin import setup_admin

from app.api.router import router
from app.core.config import settings
from app.admin.main import admin_app


app = FastAPI(
    debug=settings.project.debug,
    title=settings.project.title,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

add_pagination(app)
app.include_router(router)
setup_admin(
    admin_app=admin_app,
    app=app,
)

logger.info(f'Running {settings.project.title}')
logger.info(f'API running on: {settings.project.backend_url}')
logger.info(f'Swagger url: {settings.project.backend_url}/docs/')
