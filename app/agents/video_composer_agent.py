from pathlib import Path

from app.agents.base_agent import BaseAgent
from app.models.job_context import JobContext
from app.services.ffmpeg_service import FFmpegService


class VideoComposerAgent(BaseAgent):

    name = "VideoComposerAgent"

    def __init__(self):

        self.ffmpeg = FFmpegService()

    def execute(
        self,
        context: JobContext,
    ):

        if context.downloaded_video is None:
            return self.failure(
                context,
                "Downloaded video not found."
            )

        if context.local_audio is None:
            return self.failure(
                context,
                "Narration audio not found."
            )

        output_file = (
            Path("output")
            / "video_with_new_audio.mp4"
        )

        self.ffmpeg.compose_video(
            video_path=context.downloaded_video,
            audio_path=context.local_audio,
            output_path=output_file,
        )

        context.video_with_new_audio = output_file

        return self.success(context)