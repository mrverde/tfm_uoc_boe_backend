import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from unicodedata import normalize
from markdownify import markdownify as md

URL_BOE = 'https://boe.es'
API_XML = '/diario_boe/xml.php?id=BOE-S-'


def get_boe_summary_content(str_date: str):
    """
    str_date -> Published BOE date in format yyyymmdd
    """
    x = requests.get(URL_BOE + API_XML + str_date)
    assert x.status_code == 200

    return BeautifulSoup(x.text, features="xml")


def process_boe_summary_info(content: BeautifulSoup) -> (list, list):

    if content.find('error'):
        return None

    col_names = ["fecha", "sc_num", "sc_nombre", "dp_nombre", "dp_etq", "ep_nombre", "it_id", "it_control", "it_titulo", "it_url_pdf", "it_url_htm", "it_url_xml"]
    data = []

    fecha = content.find('meta').findChild('fecha').text
    secciones = content.find_all('seccion')

    for seccion in secciones:
        sc_num = seccion.attrs.get('num')
        sc_nombre = seccion.attrs.get('nombre')
        departamentos = seccion.find_all('departamento')

        for departamento in departamentos:
            dp_nombre = departamento.attrs.get('nombre')
            dp_etq = departamento.attrs.get('etq')
            epigrafes = departamento.find_all('epigrafe')

            for epigrafe in epigrafes:
                ep_nombre = epigrafe.attrs.get('nombre')
                items = epigrafe.find_all('item')

                for item in items:
                    it_id = item.attrs.get('id')
                    it_control = item.attrs.get('control')
                    it_titulo = item.findChild('titulo').text
                    it_url_pdf = item.findChild('urlPdf').text
                    it_url_htm = item.findChild('urlHtm').text
                    it_url_xml = item.findChild('urlXml').text

                data.append([fecha, sc_num, sc_nombre, dp_nombre, dp_etq, ep_nombre, it_id, it_control, it_titulo, it_url_pdf, it_url_htm, it_url_xml])

    return data, col_names


def extract_boe_summary_info(
    day: int|None= None, day_end: int|None= None,
     month: int|None= None, month_end: int|None= None,
     year: int|None= None, year_end: int|None= None,
     export_pandas: bool=False,
) -> list|None:
    """
    This funcion iterates over a range of dates and get the data for those period of time
    params and returns the summary of boe data.

    Gets the boe for the current day if no data is passed.

    If export_pandas is true a csv file with the scrapped data is generated
    """

    day = day or datetime.now().day
    day_end = day_end or day or datetime.now().day
    month = month or datetime.now().month
    month_end = month_end or month or datetime.now().month
    year = year or datetime.now().year
    year_end = year_end or year or datetime.now().year

    complete_data = []

    for year in range(year, year_end + 1):
        for month in range(month, month_end + 1):
            for day in range(day, day_end + 1):
                boe_summary = get_boe_summary_content(f'{str(year)}{str(month).zfill(2)}{str(day).zfill(2)}')
                output = process_boe_summary_info(boe_summary)

                if not output:
                    print("No data for the requested date")
                else:
                    complete_data += output[0]

    if export_pandas:
        pd_complete_data = pd.DataFrame(data=complete_data, columns=output[1])
        if not pd_complete_data.empty:
            pd_complete_data.to_csv("output_boe.csv", index=False, sep="|")

    return complete_data


def generate_boe_document(boe_summary: list, export_txt:None|bool= None) -> list:
    """
    Takes the result of extract_boe_summary_info and extracts all the documents for each boe summary registry
    """
    complete_docs = []

    for boe in boe_summary:
        #print(URL_BOE + boe[11])
        x = requests.get(URL_BOE + boe[11])
        assert x.status_code == 200

        boe_document = BeautifulSoup(x.text, features="xml")

        out_txt = ""

        out_txt += f"IDENTIFICADOR: {boe_document.find('identificador').text}\n"
        out_txt += f"ORIGEN: {boe_document.find('origen_legislativo').text}\n"
        out_txt += f"DEPARTAMENTO: {boe_document.find('departamento').text}\n"
        out_txt += f"RANGO: {boe_document.find('rango').text}\n"
        out_txt += f"TITULO: {boe_document.find('titulo').text}\n"

        for txt in boe_document.css.select('documento > texto')[0].children:
            if hasattr(txt, 'attrs') and len(txt.attrs) > 0:
                if 'tabla' in txt.get('class'):
                    t_header = txt.find('caption')
                    if t_header:
                        t_header = t_header.text.replace('\n', '')
                        out_txt += f"TABLA: {t_header}\n"

                    col_names = txt.find('colgroup')
                    if col_names:
                        col_names_vals = set(col_names.text.split("\n"))
                        if col_names_vals == 1 and '' in col_names_vals:
                            col_names = md(str(txt.find('colgroup'))).replace('\n', '')
                            out_txt += f"{col_names}\n"

                    for row in txt.find_all('tr'):
                        row_v = md(str(row)).replace("\n", "").replace("||", "|\n|")
                        out_txt += f"{md(str(row_v))}\n"

                elif 'parrafo' not in txt.get('class'):
                    out_txt += f"\n{txt.text}\n"

                else:
                    out_txt += txt.text

            else:
                out_txt += txt.text

        out_txt = normalize("NFKD", out_txt).replace(".o", "º").replace("\\\\*", "").replace("\\*", "")

        if export_txt:
            if not os.path.exists('output'):
                os.makedirs('output')

            with open(f"output/{boe[0][6:] + boe[0][3:5] + boe[0][0:2]}_{boe[6]}.txt", "w") as text_file:
                text_file.write(out_txt)

        complete_docs.append(out_txt)

    return complete_docs


def process_date_yyyymmdd_to_vars(date:str|None) -> tuple:

    year, month, day = None, None, None

    if date:
        assert len(date) == 8, "Date should have 8 characters in format yyyymmdd"
        year = int(date[0:4])
        month = int(date[4:6])
        day = int(date[6:])

    return year, month, day
