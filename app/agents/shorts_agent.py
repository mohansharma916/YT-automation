from app.agents.base_agent import BaseAgent
from app.models.job_context import JobContext
from app.providers.factory.provider_factory import ProviderFactory


class ShortsAgent(BaseAgent):

    name = "ShortsAgent"

    def __init__(self):

        self.provider = ProviderFactory.create()

    def execute(self, context: JobContext):

         shorts = self.provider.generate_shorts(
        context.subtitle
     )
         context.shorts = shorts
         return self.success(context)