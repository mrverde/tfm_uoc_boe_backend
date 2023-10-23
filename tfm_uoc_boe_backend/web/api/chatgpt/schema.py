from pydantic import BaseModel


class ChatGPTBoeResumeInput(BaseModel):
    """Simple chatgpt model."""

    boeText: str


class ChatGPTResumeOutput(BaseModel):
    """Model for the response of ChatGPT resume"""

    topics: list[str]
    resume: str
