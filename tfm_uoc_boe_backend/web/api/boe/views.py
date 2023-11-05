from fastapi import APIRouter
from tfm_uoc_boe_backend.services.boe import generate_boe_resumes, extract_boe_summary_info, process_date_yyyymmdd_to_vars, generate_boe_resume

from tfm_uoc_boe_backend.web.api.boe.schema import Boe

router = APIRouter()

@router.get("/")
async def get_boe(boe_xml_address: str) -> str:
    """
    Obtains a processed boe document using the xml address of each document.

    :param boe_xml_address: str

    :returns: A str with the boe text
    """

    return generate_boe_resume(boe_xml_address)


@router.get("/getall")
async def get_all_boe_data(date:None|str=None) -> list:
    """
    Obtains the complete content of all the BOEs of a specific day.
    If the date parameter is not provided, it returns those of the current day.

    :param date: in yyyymmdd format

    :returns: A list with the content of all the BOEs
    """

    year, month, day = process_date_yyyymmdd_to_vars(date)

    return generate_boe_resumes(extract_boe_summary_info(day=day, month=month, year=year))


@router.get("/summary")
async def get_boe_data_summary(date:None|str=None) -> list:
    """
    Obtains a summary for all the BOEs of a specific day.
    If the date parameter is not provided, it returns those of the current day.

    :param date: in yyyymmdd format

    :returns: A lists with the summary of each BOE document
    """

    year, month, day = process_date_yyyymmdd_to_vars(date)

    return extract_boe_summary_info(day=day, month=month, year=year)
