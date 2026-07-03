from app.agents.base_agent import BaseAgent
from app.models.job_context import JobContext
from app.providers.factory.ai_provider_factory import AIProviderFactory



class MetadataAgent(BaseAgent):

    name = "MetadataAgent"

    def __init__(self):

        self.provider = AIProviderFactory.create()

    def execute(
        self,
        context: JobContext,
    ):

        metadata = self.provider.generate_metadata(
            subtitle=context.subtitle,
            shorts=context.shorts,
        )

        context.metadata_ai = metadata

        return self.success(context)