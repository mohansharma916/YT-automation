from pathlib import Path

from app.agents.base_agent import BaseAgent
from app.models.job_context import JobContext
from app.services.ffmpeg_service import FFmpegService
from app.services.youtube_service import YoutubeService


class DownloadAgent(BaseAgent):

    name = "DownloadAgent"

    def __init__(self):

        self.ffmpeg = FFmpegService()
        self.youtube = YoutubeService()

    def execute(
        self,
        context: JobContext,
    ):

        self.log_start()

        if context.local_audio is None:
            raise ValueError("Audio not found.")

        ####################################################
        # Audio Duration
        ####################################################

        duration = self.ffmpeg.get_duration(
            context.local_audio,
        )

        context.audio_duration = duration

        ####################################################
        # Download Background Video
        ####################################################
        background = self.youtube.download_background_video(
            url=context.background_video_url,
            duration=duration + 30,
        )

    

        ####################################################
        # Remove Audio
        ####################################################

        silent = Path("downloads/background.mp4")

        self.ffmpeg.remove_audio(
            background,
            silent,
        )

        context.background_video = silent

        return self.success(
            context,
        )