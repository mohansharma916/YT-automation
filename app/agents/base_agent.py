from abc import ABC, abstractmethod
from multiprocessing import context
from app.models.agent_result import AgentResult
from app.models.job_context import JobContext
from app.utils.logger import logger


class BaseAgent(ABC):

    name = "BaseAgent"

    @abstractmethod
    def execute(self, *args, **kwargs) -> AgentResult:
        pass

    def success(self, context: JobContext):

        logger.success(f"[{self.name}] Completed")

        return AgentResult(
        success=True,
        context=context,
         )

    def failure(self,context: JobContext,error: str):


        logger.error(f"[{self.name}] {error}")

        return AgentResult(
        success=False,
        context=context,
        error=error,
    )

    def log_start(self):
        logger.info(f"[{self.name}] Started")

    def log_finish(self):
        logger.info(f"[{self.name}] Finished")

    