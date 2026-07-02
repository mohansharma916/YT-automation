from pydantic import BaseModel


class SubtitleTheme(BaseModel):

    font: str

    font_size: int

    primary_color: str

    secondary_color: str

    outline_color: str

    back_color: str

    bold: bool

    italic: bool

    outline: int

    shadow: int

    alignment: int

    margin_left: int

    margin_right: int

    margin_vertical: int