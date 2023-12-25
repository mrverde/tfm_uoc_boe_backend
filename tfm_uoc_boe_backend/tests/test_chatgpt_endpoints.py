import pytest
import requests
from fastapi.testclient import TestClient
from unittest.mock import patch
import openai
import json

CHATGPT_RESPONSE = {
  "id": "chatcmpl-8Zejf5FyFXA7OYjnrnh9TMtzdP31x",
  "object": "chat.completion",
  "created": 1703508759,
  "model": "gpt-3.5-turbo-16k-0613",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "TEMAS: Ministerio Fiscal | Nombramiento de Fiscal Decano | Coordinaci\u00f3n y direcci\u00f3n de la Secci\u00f3n Especializada Antidroga | Procedimiento Administrativo | Recursos administrativos y contencioso-administrativos\n\nRESUMEN: El Decreto de 5 de diciembre de 2023, emitido por el Fiscal General del Estado, nombra a don Adria\u0301n Salazar Larracoechea como Fiscal Decano en la Fiscali\u0301a Superior de Illes Balears, para la coordinacio\u0301n y direccio\u0301n de la Seccio\u0301n Especializada Antidroga. El nombramiento se realiza tras la jubilaci\u00f3n del anterior fiscal decano y se basa en la propuesta motivada del Fiscal Jefe y en la solicitud del candidato, quien cuenta con la formaci\u00f3n, experiencia y m\u00e9ritos necesarios para el cargo. El procedimiento de nombramiento cumple con los requisitos establecidos en el Estatuto Orga\u0301nico del Ministerio Fiscal y en el Reglamento del Ministerio Fiscal. El Decreto tambi\u00e9n establece los recursos administrativos y contencioso-administrativos que se pueden interponer contra la decisi\u00f3n.",
      },
      "logprobs": None,
      "finish_reason": "stop",
    },
  ],
  "usage": {
    "prompt_tokens": 2073,
    "completion_tokens": 264,
    "total_tokens": 2337,
  },
  "system_fingerprint": None,
}

REQUEST_MESSAGE = [{'role': 'user', 'content': 'Vas a ayudar al equipo legal de nuestra empresa. Para ello te vamos a pasar un texto jurídico en el espacio delimitado entre triples comillas.\n\nDentro del texto encontrarás al principio varias características que explico en la siguiente enumeración:\n\n1) Un código identificador a continuación de la palabra IDENTIFICADOR:\n\n2) Su origena a continuación de la palabra ORIGEN:\n\n3) El departamento a continuación de la palabra DEPARTAMENTO:\n\n4) El rango legal del texto a continuación de la palabra RANGO:\n\n5) El título del texto jurídico a continuación de la palabra TITULO:\n\nTras estos cinco elementos está el contenido del texto jurídico. Es posible que existan tablas dentro del texto. Estas tablas pueden identificarse porque sus columnas están delimitadas por el carácter |. El encabezado de la tabla estará separado por una fila que tendrá el siguiente formato | --- | --- |. Un ejemplo de una tabla de 3 filas y 3 columnas con este formato es el siguiente:\n\n|Encabezado 1|Encabezado 2|Encabezado 3|\n| --- | --- | --- |\n|fila 1 dato 1|fila 1 dato 2|fila 1 dato 3|\n|fila 2 dato 1|fila 2 dato 2|fila 2 dato 3|\n\nTu primera tarea va a ser seleccionar un máximo de diez temas que sirvan para saber el contenido del texto. Uno de los temas será siempre el departamento. Los temas los pondrás a continuación de la palabra TEMAS: y estarán separados por el carácter "|"\n\nTu segunda tarea va a ser generar un resumen del texto que extraiga las ideas principales de su contenido en un máximo de 700 palabras. El resumen aparecerá a continuación de la palabra RESUMEN:\n\n```boeText=\'string\'```\n'}]

RESPONSE_OK = '{"topics":["Ministerio Fiscal","Nombramiento de Fiscal Decano","Coordinación y dirección de la Sección Especializada Antidroga","Procedimiento Administrativo","Recursos administrativos y contencioso-administrativos"],"resume":"El Decreto de 5 de diciembre de 2023, emitido por el Fiscal General del Estado, nombra a don Adrián Salazar Larracoechea como Fiscal Decano en la Fiscalía Superior de Illes Balears, para la coordinación y dirección de la Sección Especializada Antidroga. El nombramiento se realiza tras la jubilación del anterior fiscal decano y se basa en la propuesta motivada del Fiscal Jefe y en la solicitud del candidato, quien cuenta con la formación, experiencia y méritos necesarios para el cargo. El procedimiento de nombramiento cumple con los requisitos establecidos en el Estatuto Orgánico del Ministerio Fiscal y en el Reglamento del Ministerio Fiscal. El Decreto también establece los recursos administrativos y contencioso-administrativos que se pueden interponer contra la decisión.","status":"ok"}'

GET_BOE_BODY_RESPONSE = '<?xml version="1.0" encoding="UTF-8"?>\n<documento fecha_actualizacion="20231225071519">\n  <metadatos>\n    <identificador>BOE-A-2023-26170</identificador>\n    <origen_legislativo codigo="1">Estatal</origen_legislativo>\n    <departamento codigo="4510">Ministerio Fiscal</departamento>\n    <rango codigo="1510">Decreto</rango>\n    <fecha_disposicion>20231205</fecha_disposicion>\n    <numero_oficial/>\n    <titulo>Decreto de 5 de diciembre de 2023, del Fiscal General del Estado, por el que se nombra Fiscal Decano en la Fiscalía Superior de Illes Balears, para la coordinación y dirección de la Sección Especializada Antidroga, a don Adrián Salazar Larracoechea.</titulo>\n    <diario codigo="BOE">Boletín Oficial del Estado</diario>\n    <fecha_publicacion>20231225</fecha_publicacion>\n    <diario_numero>307</diario_numero>\n    <seccion>2</seccion>\n    <subseccion>A</subseccion>\n    <pagina_inicial>171113</pagina_inicial>\n    <pagina_final>171114</pagina_final>\n    <suplemento_pagina_inicial/>\n    <suplemento_pagina_final/>\n    <url_pdf>/boe/dias/2023/12/25/pdfs/BOE-A-2023-26170.pdf</url_pdf>\n    <url_epub/>\n    <url_pdf_catalan/>\n    <url_pdf_euskera/>\n    <url_pdf_gallego/>\n    <url_pdf_valenciano/>\n    <estatus_legislativo/>\n    <fecha_vigencia/>\n    <estatus_derogacion>N</estatus_derogacion>\n    <fecha_derogacion/>\n    <judicialmente_anulada>N</judicialmente_anulada>\n    <fecha_anulacion/>\n    <vigencia_agotada>N</vigencia_agotada>\n    <estado_consolidacion codigo=""/>\n    <letra_imagen>A</letra_imagen>\n    <suplemento_letra_imagen/>\n  </metadatos>\n  <analisis>\n    <materias/>\n    <notas/>\n    <referencias>\n      <anteriores/>\n      <posteriores/>\n    </referencias>\n    <alertas/>\n  </analisis>\n  <texto>\n    <p class="centro_negrita">Hechos</p>\n    <p class="articulo">Primero.</p>\n    <p class="parrafo_2">El\xa027 de noviembre de\xa02023 se recibió en la FGE un oficio del Excmo. Sr. Fiscal Superior de la Fiscalía de la Comunidad de las Islas Baleares, remitiendo a la Inspección Fiscal un escrito en el que propuso el nombramiento del Ilmo. Sr. Fiscal don Adrián Salazar Larracoechea como decano coordinador encargado del área especializada antidroga en la Fiscalía Superior. El Sr. Salazar Larracoechea es actualmente fiscal delegado de la Fiscalía Especial Antidroga en el mismo órgano fiscal.</p>\n    <p class="parrafo">El escrito venía complementado por la justificación de que el Excmo. Sr. Fiscal Superior había comunicado a toda la plantilla la oferta de la plaza, a la que ha concurrido un solo interesado. La propuesta del Fiscal Superior se acompaña también de la solicitud y el currículo profesional del único candidato, mostrando su parecer favorable a la designación del Ilmo. Sr. don Adrián Salazar Larracoechea, ponderando los méritos que posee para desempeñar el cargo.</p>\n    <p class="articulo">Segundo.</p>\n    <p class="parrafo">Con motivo de la jubilación de la anterior fiscal decana para esa coordinación en la Fiscalía de la Comunidad de Islas Baleares, el Fiscal Superior comunicó a todos los miembros de la plantilla que quien estuviera interesado debía formular la correspondiente solicitud. El único solicitante ha aportado su <em>curriculum vitae </em>y tiene acreditada suficiente experiencia y formación, por lo que el Fiscal Superior propone a don Adrián Salazar Larracoechea, justificando la decisión. La solicitud con la propuesta favorable ha sido elevada por el Fiscal Superior a la Inspección de la Fiscalía General del Estado, destacando los méritos que hacen a don Adrián idóneo para desempeñar el cargo.</p>\n    <p class="parrafo">Por tanto, constan la propuesta del Excmo. Sr. Fiscal Superior remitida a la Inspección Fiscal, habiendo sido oído en el mismo sentido el Consejo Fiscal [artículo\xa03.d) del Real Decreto 437/1983].</p>\n    <p class="centro_negrita">Fundamentos de Derecho</p>\n    <p class="articulo">Primero.</p>\n    <p class="parrafo">El Estatuto Orgánico del Ministerio Fiscal dispone que los fiscales decanos de las Fiscalías serán nombrados mediante resolución dictada por el Fiscal General del Estado, a propuesta motivada del Fiscal Jefe respectivo. El mismo precepto exige que, para la cobertura de estos cargos y con carácter previo, se realice una convocatoria entre los fiscales de la plantilla, así como que la propuesta se acompañe de una relación de todos los que lo hayan solicitado, con aportación de los méritos alegados (artículo\xa036.4).</p>\n    <p class="parrafo">Por su parte, el artículo\xa061 del Reglamento del Ministerio Fiscal (Real Decreto 305/2022, de\xa03 de mayo), establece que los fiscales decanos a los que se refiere el artículo\xa036.4 EOMF serán nombrados, tras convocatoria pública entre los fiscales de la plantilla, mediante Decreto de la persona titular de la Fiscalía General del Estado previa propuesta motivada del Fiscal Jefe, remitida a través de la Inspección Fiscal, que ha elevado informe favorable a la propuesta formulada. Ha sido oído el Consejo Fiscal.</p>\n    <p class="parrafo">En la solicitud informada, el solicitante ha acreditado formación, méritos e idoneidad para desempeño del contenido funcional concreto que le asigna a la plaza.</p>\n    <p class="articulo">Segundo.</p>\n    <p class="parrafo">Se han llevado a cabo, por tanto, todos los trámites previstos para proceder al nombramiento interesado. La propuesta informada está suficientemente motivada y avala la idoneidad del candidato propuesto. En consecuencia, vista la propuesta formulada y el informe de la Inspección Fiscal, de conformidad con las previsiones del Estatuto Orgánico del Ministerio Fiscal y del RMF, y haciendo propia la fundamentación de la propuesta, acuerdo:</p>\n    <p class="parrafo_2">1.\u2003Nombrar al Ilmo. Sr. don Adrián Salazar Larracoechea fiscal decano en la Fiscalía Superior de Islas Baleares, para la coordinación y dirección de la Sección Especializada Antidroga.</p>\n    <p class="parrafo">2.\u2003Notificar este Decreto a la Excma. Sra. Fiscal Jefa Antidroga, al Excmo. Sr. Fiscal Superior de Islas Baleares, que lo trasladará al fiscal interesado, y al Ministerio de Justicia, con entrega de copias de la resolución.</p>\n    <p class="parrafo">3.\u2003Publíquese el presente nombramiento en el «Boletín Oficial del Estado».</p>\n    <p class="parrafo">4.\u2003Contra el presente Decreto, que pone fin a la vía administrativa de conformidad con lo dispuesto en el artículo\xa0114 de la Ley\xa039/2015, de\xa01 de octubre, de Procedimiento Administrativo Común de las Administraciones Públicas, cabe interponer en el plazo de un mes recurso potestativo de reposición, a contar desde el día siguiente a su publicación ante la Fiscalía General del Estado (C/Fortuny, n° 4, Madrid\xa028010) en los términos establecidos por el artículo\xa0123 y concordantes de aquella ley o, alternativamente, recurso contencioso-administrativo ante la Sala de lo Contencioso Administrativo del Tribunal Supremo, según lo establecido en los artículos\xa010, 12 y\xa014.1 regla\xa01.ª de la Ley\xa029/1998, de\xa013 de julio, reguladora de la Jurisdicción Contencioso Administrativa, en el plazo de dos meses a contar desde el día siguiente a su publicación, conforme a lo dispuesto en el artículo\xa046 de esa misma ley.</p>\n    <p class="parrafo_2">Madrid, 5 de diciembre de\xa02023.–El Fiscal General del Estado,\xa0Álvaro García Ortiz.</p>\n  </texto>\n</documento>\n'


async def test_txtboeresume_ok(client, fastapi_app):
    client = TestClient(fastapi_app)
    url = fastapi_app.url_path_for("generate_chatgpt_boe_resume_using_txt")
    mocked_response = openai.openai_object.OpenAIObject()
    mocked_response = CHATGPT_RESPONSE

    with patch("openai.ChatCompletion.create", return_value=mocked_response) as mocked_request:
        response = client.post(url, params={"model":"gpt-3.5-turbo-16k"}, json={"boeText": "string"})

    model = mocked_request.call_args_list[0][1]["model"]
    messages = mocked_request.call_args_list[0][1]["messages"]

    assert mocked_request.call_count == 1
    assert model == "gpt-3.5-turbo-16k"
    assert messages == REQUEST_MESSAGE
    assert response.status_code == 200
    assert response.text == RESPONSE_OK


@pytest.mark.parametrize(
    "error,resume", [
        (
            openai.InvalidRequestError("This model's maximum context length is 1 tokens. However, your messages resulted in 1 tokens. Please reduce the length of the messages.", "param"),
            "Too long BOE: This model's maximum context length is 1 tokens. However, your messages resulted in 1 tokens. Please reduce the length of the messages.",
        ),
        (
            openai.error.RateLimitError("Request too large for gpt-3.5-turbo-16k in organization org on tokens_usage_based per min: Limit 60000, Requested 65155. Visit https://platform.openai.com/account/rate-limits to learn more.", "param"),
            "Rate Limit Error: Request too large for gpt-3.5-turbo-16k in organization org on tokens_usage_based per min: Limit 60000, Requested 65155. Visit https://platform.openai.com/account/rate-limits to learn more.",
        ),
    ],
)
async def test_txtboeresume_ko(client, fastapi_app, error, resume):
    client = TestClient(fastapi_app)
    url = fastapi_app.url_path_for("generate_chatgpt_boe_resume_using_txt")

    with patch("openai.ChatCompletion.create", side_effect=error) as mocked_request:
        response = client.post(url, params={"model":"gpt-3.5-turbo-16k"}, json={"boeText": "string"})

    rp = json.loads(response.text)
    assert mocked_request.call_count == 1
    assert len(rp.keys()) == 3
    assert rp["topics"] == []
    assert rp["status"] == "error"
    assert rp["resume"] == resume


async def test_xmlboeresume(client, fastapi_app):
    client = TestClient(fastapi_app)
    url = fastapi_app.url_path_for("generte_chatgpt_boe_resume_using_xml")

    mocked_response_get = requests.Response()
    mocked_response_get.status_code = 200
    mocked_response_get._content = GET_BOE_BODY_RESPONSE.encode('utf-8')

    mocked_response = openai.openai_object.OpenAIObject()
    mocked_response = CHATGPT_RESPONSE

    with patch("requests.get", return_value=mocked_response_get) as mocked_request, \
        patch("openai.ChatCompletion.create", return_value=mocked_response) as mocked_openai:
        response = client.get(url, params={"boe_xml_address":"/diario_boe/xml.php?id=BOE-A-2023-23608"})

    model = mocked_openai.call_args_list[0][1]["model"]
    messages = mocked_openai.call_args_list[0][1]["messages"][0]["content"]

    assert mocked_request.call_count == 1
    assert mocked_openai.call_count == 1

    assert model == "gpt-3.5-turbo-16k"
    assert response.status_code == 200
    assert response.text == RESPONSE_OK
