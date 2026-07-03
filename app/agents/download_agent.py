from pathlib import Path

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

        logger.info(
            f"Downloading video: {context.youtube_url}"
        )

        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "outtmpl": str(output_dir / "%(title)s.%(ext)s"),
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

        context.downloaded_video = downloaded_video

        context.metadata["title"] = info["title"]
        context.metadata["video_id"] = info["id"]
        context.metadata["channel"] = info["uploader"]
        context.metadata["duration"] = info["duration"]

        logger.info(
            f"Downloaded video: {downloaded_video}"
        )

        return self.success(context)