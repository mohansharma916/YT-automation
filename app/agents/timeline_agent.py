from app.agents.base_agent import BaseAgent
from app.models.job_context import JobContext
from app.services.ffmpeg_service import FFmpegService
from app.services.timeline_service import TimelineService


class TimelineAgent(BaseAgent):

    name = "TimelineAgent"

    def __init__(self):

        self.ffmpeg = FFmpegService()
        self.timeline = TimelineService()

    def execute(
        self,
        context: JobContext,
    ):

        self.log_start()

        if context.local_audio is None:
            raise ValueError("Audio not found.")

        duration = self.ffmpeg.get_duration(
            context.local_audio,
        )

        print(f"Audio Duration : {duration:.2f} sec")

        context.video_parts = self.timeline.split(
            duration=duration,
            part_duration=300,
        )

        print(
            f"Total Parts : {len(context.video_parts.parts)}"
        )

        return self.success(context)