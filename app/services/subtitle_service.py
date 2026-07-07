import json
from pathlib import Path
from app.models.subtitle import Subtitle
from app.models.subtitle import SubtitleSegment


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





    def export_ass(
    self,
    subtitle,
    output_file: Path,
    vertical: bool):
        

        output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )


        print("=" * 50)
        print("EXPORT ASS")
        print("Vertical:", vertical)
        print("Output:", output_file)
        print("=" * 50)

    ####################################################
    # Style
    ####################################################

        if vertical:

        

            play_res_x = 1080
            play_res_y = 1920

            x = 540
            y = 900

            style = self.short_style()

            words_per_line = 18

        else:

            play_res_x = 1920
            play_res_y = 1080

            x = 960
            y = 430

            words_per_line = 35

            style = self.long_style()

    ####################################################
    # Header
    ####################################################

        lines = [

            "[Script Info]",
            "Title: Youtube Agent",
            "ScriptType: v4.00+",
            f"PlayResX: {play_res_x}",
            f"PlayResY: {play_res_y}",
            "ScaledBorderAndShadow:yes",
            "",

            "[V4+ Styles]",

            "Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding",

            style,

        "",

        "[Events]",

        "Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text",
    ]

    ####################################################
    # Dialogue
    ####################################################

        for segment in subtitle.segments:


            text = self.wrap_words(
            segment.text,
            words_per_line,
        )

            lines.append(

            "Dialogue: 0,"

            f"{self.ass_time(segment.start)},"

            f"{self.ass_time(segment.end)},"

            "Default,,0,0,0,,"

            f"{{\\an5\\pos({x},{y})\\fad(120,120)}}"

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
    


    def long_style(self):

        return (
        "Style: Default,"
        "Noto Serif Devanagari ExtraBold,"
        "98,"
        "&H00FFFFFF,"
        "&H0000FFFF,"
        "&H00000000,"
        "&H96000000,"
        "-1,0,0,0,"
        "100,100,0,0,"
        "1,6,0,5,"
        "0,0,0,1"
    )


    def short_style(self):

         return (
        "Style: Default,"
        "Noto Serif Devanagari ExtraBold,"
        "96,"
        "&H00FFFFFF,"
        "&H0000FFFF,"
        "&H00000000,"
        "&H96000000,"
        "-1,0,0,0,"
        "100,100,0,0,"
        "1,6,0,5,"
        "0,0,0,1"
    )


    def wrap_words(
    self,
    text: str,
    max_chars: int = 18,):
        words = text.split()

        lines = []
        current = ""

        for word in words:

            candidate = word if not current else f"{current} {word}"

            if len(candidate) <= max_chars:
                current = candidate
            else:
                lines.append(current)
                current = word

            if current:
                lines.append(current)

    # Maximum 2 lines
        if len(lines) > 2:
            lines = [
                " ".join(words[: len(words)//2]),
                " ".join(words[len(words)//2 :]),
            ]

        return r"\N".join(lines)