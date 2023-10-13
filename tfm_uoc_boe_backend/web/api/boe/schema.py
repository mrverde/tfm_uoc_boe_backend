from pydantic import BaseModel


class Boe(BaseModel):
    """Simple boe model."""

    boe: str
