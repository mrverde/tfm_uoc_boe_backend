import openai
import os
import re

from dotenv import load_dotenv, find_dotenv
from tfm_uoc_boe_backend.services.common import read_txt_file

load_dotenv(find_dotenv())

openai.api_key  = os.getenv('OPENAI_API_KEY')

CHATGPT_MODELS_ALLOWED = ["gpt-4", "gpt-4-32k", "gpt-3.5-turbo-16k"]

def chatGPT_boe_resume(boe_document:str, model:str) -> str:

    assert model in CHATGPT_MODELS_ALLOWED

    prompt = read_txt_file("tfm_uoc_boe_backend/web/assets/prompts/boe_resume.txt").format(text=boe_document)

    messages = [{"role": "user", "content": prompt}]

    try:
        response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
        )

        return split_response_in_topics_and_resume(response.choices[0].message["content"])

    except openai.InvalidRequestError as e:
        return f"Too long BOE: {e}"


def split_response_in_topics_and_resume(chatgpt_response):
    resume_word = "RESUMEN:"
    resume = chatgpt_response[chatgpt_response.find(resume_word) + len(resume_word):]
    resume = re.sub(r"^\W+", "", resume)

    topics = chatgpt_response[ :chatgpt_response.find(resume_word)].split("|")


    tr = [(r"^TEMAS:\s+", ""), (r"^\W+", ""), (r"\W+$", "")]
    for regex, repl in tr:
        for idx, topic in enumerate(topics):
            topics[idx] = re.sub(regex, repl, topic)

    return {"topics": topics, "resume": resume}
