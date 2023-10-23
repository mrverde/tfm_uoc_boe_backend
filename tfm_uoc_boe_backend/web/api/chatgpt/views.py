from fastapi import APIRouter
from tfm_uoc_boe_backend.services.chatgpt import chatGPT_boe_resume

from tfm_uoc_boe_backend.web.api.chatgpt.schema import ChatGPTBoeResumeInput, ChatGPTResumeOutput

router = APIRouter()


@router.post("/chatgptboeresume")
async def get_chatgpt_boe_resume(boe_document:ChatGPTBoeResumeInput, model:str="gpt-3.5-turbo-16k") -> ChatGPTResumeOutput:
    """
    This endpoint process a boe document with chatGPT and returns 10 main topics and a resume.


    """

    return chatGPT_boe_resume(boe_document, model)
