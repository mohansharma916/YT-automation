import json
from pathlib import Path



from app.models.subtitle import Subtitle
from app.models.subtitle import SubtitleSegment
from app.renderers.ass_renderer import ASSRenderer


class SubtitleService:

    ####################################################
    # Basic Operations
    ####################################################

    def cut(
        self,
        subtitle: Subtitle,
        start: float,
        end: float,
    ) -> Subtitle:

        segments = []

        for segment in subtitle.segments:

            if segment.end < start:
                continue

            if segment.start > end:
                continue

            segments.append(
                SubtitleSegment(
                    start=max(segment.start, start),
                    end=min(segment.end, end),
                    text=segment.text,
                )
            )

        return Subtitle(
            segments=segments,
        )

    def shift(
        self,
        subtitle: Subtitle,
        seconds: float,
    ) -> Subtitle:

        return Subtitle(

            segments=[

                SubtitleSegment(

                    start=segment.start + seconds,

                    end=segment.end + seconds,

                    text=segment.text,

                )

                for segment in subtitle.segments

            ]

        )

    def normalize(
        self,
        subtitle: Subtitle,
    ) -> Subtitle:

        if len(subtitle.segments) == 0:
            return subtitle

        offset = subtitle.segments[0].start

        return self.shift(
            subtitle,
            -offset,
        )

    ####################################################
    # Merge
    ####################################################

    def merge(
        self,
        first: Subtitle,
        second: Subtitle,
    ) -> Subtitle:

        return Subtitle(

            segments=[

                *first.segments,

                *second.segments,

            ]

        )

    ####################################################
    # Long Video Subtitle
    ####################################################

    def create_final_subtitle(
        self,
        subtitle: Subtitle,
        hook_start: float,
        hook_end: float,
    ) -> Subtitle:

        hook = self.cut(
            subtitle,
            hook_start,
            hook_end,
        )

        hook = self.normalize(
            hook,
        )

        hook_duration = hook_end - hook_start

        original = self.shift(
            subtitle,
            hook_duration,
        )

        return self.merge(
            hook,
            original,
        )

    ####################################################
    # Shorts
    ####################################################

    def create_short_subtitle(
        self,
        subtitle: Subtitle,
        start: float,
        end: float,
    ) -> Subtitle:

        short = self.cut(
            subtitle,
            start,
            end,
        )

        return self.normalize(
            short,
        )

    ####################################################
    # Save
    ####################################################

    def save_json(
        self,
        subtitle: Subtitle,
        output: Path,
    ):

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output.write_text(

            json.dumps(

                subtitle.model_dump(),

                ensure_ascii=False,

                indent=4,

            ),

            encoding="utf-8",

        )

    # def save_ass(
    #     self,
    #     subtitle: Subtitle,
    #     output: Path,
    # ):

    #     output.parent.mkdir(
    #         parents=True,
    #         exist_ok=True,
    #     )

    #     ASSRenderer().render(
    #         subtitle,
    #         output,
    #     )


  


    def export_ass(
    self,
    subtitle,
    output_file: Path,):
        

        output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

        lines = []

        lines.append("[Script Info]")
        lines.append("Title: Youtube Agent")
        lines.append("ScriptType: v4.00+")
        lines.append("PlayResX: 1920")
        lines.append("PlayResY: 1080")
        lines.append("WrapStyle: 2")
        lines.append("ScaledBorderAndShadow: yes")
        lines.append("")

        lines.append("[V4+ Styles]")
        lines.append(
        "Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding"
    )

        lines.append(
        "Style: Default,Poppins ExtraBold,90,&H00FFFFFF,&H0000FFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,5,0,5,0,0,0,1"
    )

        lines.append("")
        lines.append("[Events]")
        lines.append(
        "Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text"
    )

        for segment in subtitle.segments:

            text = self.format_text(segment.text)

            lines.append(
            "Dialogue: 0,"
            f"{self.ass_time(segment.start)},"
            f"{self.ass_time(segment.end)},"
            "Default,,0,0,0,,"
            "{\\an5\\pos(960,430)\\fad(150,150)}"
            f"{text}"
        )

        output_file.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    def ass_time(
    self,
    seconds: float,):

        hours = int(seconds // 3600)

        minutes = int((seconds % 3600) // 60)

        secs = seconds % 60

        return f"{hours}:{minutes:02}:{secs:05.2f}"
    

    def format_text(
    self,
    text: str,):
        

        words = text.split()

        if len(words) <= 3:
            return text

        result = []

        line = []

        for word in words:

            line.append(word)

        if len(line) == 3:

            result.append(
                " ".join(line)
            )

            line = []

        if line:

            result.append(
            " ".join(line)
        )

        return r"\N".join(result)