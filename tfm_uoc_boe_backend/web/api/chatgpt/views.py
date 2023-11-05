from fastapi import APIRouter
from tfm_uoc_boe_backend.services.chatgpt import chatGPT_boe_resume
from tfm_uoc_boe_backend.services.boe import generate_boe_resume

from tfm_uoc_boe_backend.web.api.chatgpt.schema import ChatGPTBoeResumeInput, ChatGPTResumeOutput

router = APIRouter()


@router.post("/txtboeresume")
async def generate_chatgpt_boe_resume_using_txt(boe_document:ChatGPTBoeResumeInput, model:str="gpt-3.5-turbo-16k") -> ChatGPTResumeOutput|str:
    """
    This endpoint process a boe document with chatGPT and returns 10 main topics and a resume.

    :param boe_document: str
    :model boe_xml_address: str

    :returns: ChatGPTResumeOutput A list of topics and a resume

    """

    return chatGPT_boe_resume(boe_document, model)

@router.get("/xmlboeresume")
async def generte_chatgpt_boe_resume_using_xml(boe_xml_address: str,  model:str="gpt-3.5-turbo-16k") -> ChatGPTResumeOutput|str:
    """
    This endpoint recieves a boe xml address and process it with chatGPT. Returns 10 main topics and a resume.

    :param boe_document: str
    :model boe_xml_address: str

    :returns: ChatGPTResumeOutput A list of topics and a resume or str if an error is raised
    """
    return chatGPT_boe_resume(generate_boe_resume(boe_xml_address), model)
