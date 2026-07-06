from app.agents.base_agent import BaseAgent
from app.models.job_context import JobContext


class TimelineComposerAgent(BaseAgent):

    name = "TimelineComposerAgent"

    def execute(self, context: JobContext):


        return self.success(context)