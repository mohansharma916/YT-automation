from pydantic import BaseModel

from app.models.job_context import JobContext


class AgentResult(BaseModel):
    success: bool
    context: JobContext
    error: str | None = None