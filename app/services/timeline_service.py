from copy import deepcopy
from pathlib import Path

from app.models.subtitle import Subtitle, SubtitleSegment
from app.models.timeline import Timeline


class TimelineService:

    def create(
        self,
        audio: Path,
        subtitle: Subtitle,
        duration: float,
    ) -> Timeline:

        return Timeline(
            audio=audio,
            subtitle=subtitle,
            duration=duration,
        )

    def shift(
        self,
        subtitle: Subtitle,
        seconds: float,
    ) -> Subtitle:

        segments = []

        for segment in subtitle.segments:

            segments.append(
                SubtitleSegment(
                    start=segment.start + seconds,
                    end=segment.end + seconds,
                    text=segment.text,
                )
            )

        return Subtitle(
            segments=segments
        )

    def trim(
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
            segments=segments
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

        result = deepcopy(first)

        result.segments.extend(
            second.segments
        )

        return result