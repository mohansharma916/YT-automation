from app.agents.base_agent import BaseAgent
from app.models.job_context import JobContext
from app.providers.factory.provider_factory import ProviderFactory


class SubtitleAgent(BaseAgent):

    name = "SubtitleAgent"

    def __init__(self):

        self.provider = ProviderFactory.create()

    def execute(
        self,
        context: JobContext,
    ):

        self.log_start()

        subtitle = self.provider.generate_subtitles(
            context.transcript
        )

        context.subtitle = subtitle

        return self.success(context)