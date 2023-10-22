from fastapi import APIRouter
from tfm_uoc_boe_backend.services.chatgpt import chatGPT

from tfm_uoc_boe_backend.web.api.chatgpt.schema import ChatGPT

router = APIRouter()


@router.get("/chatgpt")
async def get_chatgpt_response() -> dict:
    """
    This endpoint process a txt with chatgpt
    """

    return chatGPT()
