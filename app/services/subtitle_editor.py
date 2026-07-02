from app.models.subtitle import Subtitle, SubtitleSegment


class SubtitleEditor:

    def create_hook_subtitle(
        self,
        subtitle: Subtitle,
        hook_start: float,
        hook_end: float,
    ) -> Subtitle:

        hook_duration = hook_end - hook_start

        hook_segments = []
        original_segments = []

        for segment in subtitle.segments:

            # Hook subtitles
            if hook_start <= segment.start <= hook_end:

                hook_segments.append(
                    SubtitleSegment(
                        start=segment.start - hook_start,
                        end=segment.end - hook_start,
                        text=segment.text,
                    )
                )

            # Original subtitles shifted
            original_segments.append(
                SubtitleSegment(
                    start=segment.start + hook_duration,
                    end=segment.end + hook_duration,
                    text=segment.text,
                )
            )

        return Subtitle(
            segments=[
                *hook_segments,
                *original_segments,
            ]
        )