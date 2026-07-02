from pathlib import Path
import json

from app.agents.base_agent import BaseAgent
from app.models.job_context import JobContext
from app.providers.factory.provider_factory import ProviderFactory


class TranscriptionAgent(BaseAgent):

    name = "TranscriptionAgent"

    def __init__(self):
        self.provider = ProviderFactory.create()

    def execute(self, context: JobContext):

        subtitle = self.provider.transcribe(
            context.local_audio
        )

        context.subtitle = subtitle

        Path("subtitles").mkdir(exist_ok=True)

        subtitle_path = (
            Path("subtitles")
            / f"{context.local_audio.stem}.json"
        )

        subtitle_path.write_text(
            json.dumps(
                subtitle.model_dump(),
                ensure_ascii=False,
                indent=4,
            ),
            encoding="utf-8",
        )

        context.subtitle_file = subtitle_path

        return self.success(context)