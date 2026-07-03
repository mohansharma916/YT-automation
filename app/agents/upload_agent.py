from pathlib import Path

from app.agents.base_agent import BaseAgent
from app.models.job_context import JobContext
from app.services.youtube_service import YoutubeService


class UploadAgent(BaseAgent):
    name = "UploadAgent"

    def __init__(self):

        self.youtube = YoutubeService()

    def execute(
        self,
        context: JobContext,
    ):

        self.log_start()

        video_id = self.youtube.upload(
            Path("output/long/final.mp4"),
            context.metadata_ai.long_video,
        )

        print()

        print("Long Video Uploaded")

        print(video_id)

        print()

        for index, metadata in enumerate(
            context.metadata_ai.shorts,
            start=1,
        ):
            video = Path("output/shorts") / f"short_{index}" / "video.mp4"

            video_id = self.youtube.upload(
                video,
                metadata,
            )

            print(
                f"Short {index} Uploaded:",
                video_id,
            )

        return self.success(context)
