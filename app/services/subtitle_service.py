import json
from pathlib import Path

from app.models.subtitle import Subtitle, SubtitleSegment
from app.renderers.ass_renderer import ASSRenderer


class SubtitleService:

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

        if not subtitle.segments:
            return subtitle

        first = subtitle.segments[0].start

        return self.shift(
            subtitle,
            -first,
        )

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

    def create_hook_subtitle(
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

        duration = hook_end - hook_start

        original = self.shift(
            subtitle,
            duration,
        )

        return self.merge(
            hook,
            original,
        )

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

    def save_ass(
        self,
        subtitle: Subtitle,
        output: Path,
    ):

        renderer = ASSRenderer()

        renderer.render(
            subtitle,
            output,
        )