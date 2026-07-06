import math

from app.models.video_part import VideoPart
from app.models.video_parts import VideoParts


class TimelineService:

    def split(
        self,
        duration: float,
        part_duration: float = 300,
    ) -> VideoParts:

        total_parts = math.ceil(
            duration / part_duration,
        )

        parts = []

        for index in range(total_parts):

            start = index * part_duration

            end = min(
                start + part_duration,
                duration,
            )

            parts.append(

                VideoPart(

                    part=index + 1,

                    start=start,

                    end=end,

                    title=f"Part {index + 1}",
                )

            )

        return VideoParts(
            parts=parts,
        )