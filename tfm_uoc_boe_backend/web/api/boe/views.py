from fastapi import APIRouter
from tfm_uoc_boe_backend.services.boe import generate_boe_document, extract_boe_summary_info, process_date_yyyymmdd_to_vars

from tfm_uoc_boe_backend.web.api.boe.schema import Boe

router = APIRouter()


@router.get("/boe")
async def get_boe_data(date:None|str=None) -> list:
    """
    Obtains the complete content of all the BOEs of a specific day.
    If the date parameter is not provided, it returns those of the current day.

    :param date: in yyyymmdd format

    :returns: A list with the content of all the BOEs
    """

    year, month, day = process_date_yyyymmdd_to_vars(date)

    return generate_boe_document(extract_boe_summary_info(day=day, month=month, year=year))


@router.get("/summaryboe")
async def get_boe_data_summary(date:None|str=None) -> list:
    """
    Obtains a summary for all the BOEs of a specific day.
    If the date parameter is not provided, it returns those of the current day.

    :param date: in yyyymmdd format

    :returns: A lists with the summary of each BOE document
    """

    year, month, day = process_date_yyyymmdd_to_vars(date)

    return extract_boe_summary_info(day=day, month=month, year=year)
