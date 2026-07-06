from pathlib import Path

from app.models.subtitle import Subtitle
from app.renderers.base_renderer import BaseSubtitleRenderer


class ASSRenderer(BaseSubtitleRenderer):

    ####################################################
    # Header
    ####################################################

    def _header(self):

        return r"""
[Script Info]
Title: Youtube Agent
ScriptType: v4.00+
WrapStyle: 2
ScaledBorderAndShadow: yes
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding

Style: Default,Poppins ExtraBold,54,&H00FFFFFF,&H0000FFFF,&H00000000,&H96000000,-1,0,0,0,100,100,0,0,1,5,0,5,120,120,80,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""

    ####################################################
    # Dialogue
    ####################################################

    def _dialogue(
        self,
        segment,
    ):

        text = self._format_text(
            segment.text,
        )

        return (
            f"Dialogue: 0,"
            f"{self._time(segment.start)},"
            f"{self._time(segment.end)},"
            "Default,,0,0,0,"
            "{\\fad(120,120)},"
            f"{text}\n"
        )

    ####################################################
    # Text Formatting
    ####################################################

    def _format_text(
        self,
        text: str,
    ):

        words = text.split()

        if len(words) <= 3:
            return text

        lines = []

        current = []

        for word in words:

            current.append(word)

            if len(current) == 3:

                lines.append(
                    " ".join(current)
                )

                current = []

        if current:

            lines.append(
                " ".join(current)
            )

        return r"\N".join(lines)

    ####################################################
    # Time
    ####################################################

    def _time(
        self,
        seconds: float,
    ):

        hours = int(seconds // 3600)

        minutes = int(
            (seconds % 3600) // 60
        )

        secs = int(seconds % 60)

        centiseconds = int(
            (seconds - int(seconds))
            * 100
        )

        return (
            f"{hours}:"
            f"{minutes:02}:"
            f"{secs:02}."
            f"{centiseconds:02}"
        )

    ####################################################
    # Render
    ####################################################

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

            file.write(
                self._header()
            )

            for segment in subtitle.segments:

                file.write(
                    self._dialogue(
                        segment
                    )
                )