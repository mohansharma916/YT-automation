from app.agents.base_agent import BaseAgent
from app.models.job_context import JobContext


class TimelineComposerAgent(BaseAgent):

    name = "TimelineComposerAgent"

    def execute(self, context: JobContext):

        print()

        print("HOOK")
        print(context.timeline.hook)

        print()

        print("SHORTS")

        for short in context.timeline.shorts.shorts:
            print(short)

        return self.success(context)