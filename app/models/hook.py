from pydantic import BaseModel


class ViralHook(BaseModel):
    start: float
    end: float
    hook: str
    reason: str
    score: int