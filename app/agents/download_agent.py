from pathlib import Path
import subprocess

from yt_dlp import YoutubeDL

from app.agents.base_agent import BaseAgent
from app.models.job_context import JobContext
from app.utils.logger import logger


class DownloadAgent(BaseAgent):

    name = "DownloadAgent"

    def execute(self, context: JobContext):

        self.log_start()

        if not context.youtube_url:
            return self.failure(
                context,
                "YouTube URL not provided.",
            )

        output_dir = Path("downloads")
        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        audio_dir = Path("audio")
        audio_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        logger.info(
            f"Downloading video: {context.youtube_url}"
        )

        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "outtmpl": str(
                output_dir / "%(title)s.%(ext)s"
            ),
            "merge_output_format": "mp4",
        }

        with YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(
                context.youtube_url,
                download=True,
            )

            downloaded_video = Path(
                ydl.prepare_filename(info)
            ).with_suffix(".mp4")

        ####################################################
        # Extract Audio
        ####################################################

        audio_file = audio_dir / "sample.wav"

        command = [
            "ffmpeg",
            "-y",
            "-i",
            str(downloaded_video),
            "-vn",
            "-ac",
            "1",
            "-ar",
            "16000",
            str(audio_file),
        ]

        subprocess.run(
            command,
            check=True,
            capture_output=True,
        )

        ####################################################
        # Context
        ####################################################

        context.downloaded_video = downloaded_video
        context.local_audio = audio_file

        context.metadata["title"] = info["title"]
        context.metadata["video_id"] = info["id"]
        context.metadata["channel"] = info["uploader"]
        context.metadata["duration"] = info["duration"]

        logger.info(
            f"Downloaded video: {downloaded_video}"
        )

        logger.info(
            f"Extracted audio: {audio_file}"
        )

        return self.success(context)