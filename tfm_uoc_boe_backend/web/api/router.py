from fastapi.routing import APIRouter

from tfm_uoc_boe_backend.web.api import echo, monitoring, boe, chatgpt

BOE_VERSION = "v1"

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(boe.router, prefix=f"/{BOE_VERSION}", tags=["boe"])
api_router.include_router(chatgpt.router, prefix=f"/{BOE_VERSION}", tags=["chatGPT"])
