from pydantic import BaseModel


class ShortSegment(BaseModel):
    title: str
    start: float
    end: float
    reason: str


class Shorts(BaseModel):
    shorts: list[ShortSegment]