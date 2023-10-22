from pydantic import BaseModel


class ChatGPT(BaseModel):
    """Simple chatgpt model."""

    text: str
