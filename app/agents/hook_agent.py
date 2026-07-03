from app.agents.base_agent import BaseAgent
from app.models.job_context import JobContext
from app.providers.factory.ai_provider_factory import AIProviderFactory


class HookAgent(BaseAgent):

    name = "HookAgent"

    def __init__(self):
        self.provider = AIProviderFactory.create()

    def execute(self, context: JobContext):

        hook = self.provider.find_hook(
            context.subtitle
        )

        context.hook = hook

        return self.success(context)