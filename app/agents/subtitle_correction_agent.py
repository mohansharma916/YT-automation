import json
from pathlib import Path

from app.agents.base_agent import BaseAgent
from app.models.job_context import JobContext
from app.providers.factory.provider_factory import ProviderFactory


class SubtitleCorrectionAgent(BaseAgent):

    name = "SubtitleCorrectionAgent"

    def __init__(self):

        self.provider = ProviderFactory.llm()

    ####################################################
    # Execute
    ####################################################

    def execute(
        self,
        context: JobContext,
    ):

        self.log_start()

        print("=" * 80)
        print("CORRECTING SUBTITLES")
        print("=" * 80)

        corrected = self.provider.correct_subtitles(
            context.subtitle,
        )

        ####################################################
        # Replace Subtitle
        ####################################################

        context.subtitle = corrected

        ####################################################
        # Save Corrected Subtitle
        ####################################################

        output = Path("subtitles")

        output.mkdir(
            exist_ok=True,
        )

        corrected_file = (
            output /
            "subtitle_corrected.json"
        )

        corrected_file.write_text(

            json.dumps(

                corrected.model_dump(),

                ensure_ascii=False,

                indent=4,

            ),

            encoding="utf-8",

        )

        print("=" * 80)
        print("SUBTITLE CORRECTION COMPLETED")
        print("=" * 80)

        return self.success(
            context,
        )