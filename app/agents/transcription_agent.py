import json
from pathlib import Path

from app.agents.base_agent import BaseAgent
from app.models.job_context import JobContext
from app.providers.factory.provider_factory import ProviderFactory



class TranscriptionAgent(BaseAgent):
    name = "TranscriptionAgent"

    def __init__(self):

       self.provider = ProviderFactory.transcription()

    def execute(
        self,
        context: JobContext,
    ):

        self.log_start()

        print("=" * 50)
        print("LOCAL AUDIO :", context.local_audio)
        print("=" * 50)

        subtitle = self.provider.transcribe(
            context.local_audio,
        )

        print("Downloaded Video :", context.downloaded_video)
        print("Audio :", context.local_audio)

        context.subtitle = subtitle

        print("=" * 80)
        print("TOTAL SEGMENTS:", len(subtitle.segments))
        print("=" * 80)

        Path("subtitles").mkdir(
            exist_ok=True,
        )

        output = Path("subtitles") / "subtitle.json"

        output.write_text(
            json.dumps(
                subtitle.model_dump(),
                ensure_ascii=False,
                indent=4,
            ),
            encoding="utf-8",
        )

        context.subtitle_file = output

        return self.success(context)
