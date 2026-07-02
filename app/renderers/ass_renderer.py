from pathlib import Path

from app.models.subtitle import Subtitle
from app.renderers.base_renderer import BaseSubtitleRenderer


class ASSRenderer(BaseSubtitleRenderer):

    def _header(self):

        return """
[Script Info]
Title: Youtube Agent
ScriptType: v4.00+

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding

Style: Default,Poppins,28,&H00FFFFFF,&H0000FFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,2,1,2,20,20,40,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
""" 
    def _dialogue(
    self,
    segment,):

     return (
        f"Dialogue: 0,"
        f"{self._time(segment.start)},"
        f"{self._time(segment.end)},"
        "Default,,0,0,0,,"
        f"{segment.text}\n"
    )

    def _time(
    self,
    seconds: float,):

        hours = int(seconds // 3600)

        minutes = int(
        (seconds % 3600) // 60)

        secs = int(seconds % 60)

        centiseconds = int(
            (seconds - int(seconds))
            * 100)

        return (
        f"{hours}:"
        f"{minutes:02}:"
        f"{secs:02}."
        f"{centiseconds:02}")

    def render(
        self,
        subtitle: Subtitle,
        output_file: Path,
    ):

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            output_file,
            "w",
            encoding="utf-8",
        ) as file:

            file.write(self._header())

            for segment in subtitle.segments:

                file.write(
                    self._dialogue(segment)
                )