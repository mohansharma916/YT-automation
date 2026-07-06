from pydantic import BaseModel


class VideoPart(BaseModel):

    part: int

    start: float

    end: float

    title: str