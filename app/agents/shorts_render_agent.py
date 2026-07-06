from pathlib import Path

from app.agents.base_agent import BaseAgent
from app.models.job_context import JobContext
from app.services.shorts_editor import ShortsEditor


class ShortsRenderAgent(BaseAgent):

    name = "ShortsRenderAgent"

    def __init__(self):

        self.editor = ShortsEditor()

    def execute(
        self,
        context: JobContext,
    ):

        outputs = self.editor.create(
            video_path=context.downloaded_video,
            audio_path=context.local_audio,
            shorts=context.shorts,
            output_dir=Path("output/shorts"),
        )

        return self.success(context)