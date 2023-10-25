import os
import json
from importlib import metadata
from dotenv import load_dotenv, find_dotenv

from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from fastapi.middleware.cors import CORSMiddleware

from tfm_uoc_boe_backend.web.api.router import api_router
from tfm_uoc_boe_backend.web.lifetime import (
    register_shutdown_event,
    register_startup_event,
)

load_dotenv(find_dotenv())


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="tfm_uoc_boe_backend",
        version=metadata.version("tfm_uoc_boe_backend"),
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    app.add_middleware(
    CORSMiddleware,
    allow_origins=json.loads(os.getenv('ALLOWED_ORIGINS')),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")

    return app
