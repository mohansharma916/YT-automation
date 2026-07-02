from app.agents.base_agent import BaseAgent
from app.models.job_context import JobContext
from app.services.ffmpeg_service import FFmpegService
from app.services.timeline_service import TimelineService


class TimelineAgent(BaseAgent):

    name = "TimelineAgent"

    def __init__(self):

        self.timeline_service = TimelineService()
        self.ffmpeg = FFmpegService()

    def execute(self, context: JobContext):

        context.timeline = self.timeline_service.create(
            audio=context.local_audio,
            subtitle=context.subtitle,
            duration=self.ffmpeg.get_duration(
                context.local_audio
            ),
        )

        return self.success(context)