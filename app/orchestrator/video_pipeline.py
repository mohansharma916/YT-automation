from app.agents.hook_agent import HookAgent
from app.agents.subtitle_agent import SubtitleAgent
from app.agents.subtitle_editor_agent import SubtitleEditorAgent
from app.agents.timeline_composer_agent import TimelineComposerAgent
from app.utils.logger import logger

from app.agents.download_agent import DownloadAgent
from app.agents.transcription_agent import TranscriptionAgent
from app.agents.video_composer_agent import VideoComposerAgent
from app.agents.render_agent import RenderAgent
from app.models.agent_result import AgentResult
from app.models.job_context import JobContext
from app.agents.hook_editor_agent import HookEditorAgent
from app.agents.shorts_agent import ShortsAgent



class VideoPipeline:

    def __init__(self):

        self.agents = [
                 DownloadAgent(),

                TranscriptionAgent(),


    HookAgent(),

    ShortsAgent(),

    RenderAgent(),

        # DownloadAgent(),
        # TranscriptionAgent(),
      
        # ShortsAgent(),
        # HookEditorAgent(),
        #  SubtitleEditorAgent(),
        #     TimelineComposerAgent(),
        #       HookAgent(),
        # # VideoComposerAgent(),
        # #  ShortsRenderAgent(),
      
        # RenderAgent(),
]

    def run(self, context: JobContext) -> AgentResult:

        logger.info("Starting Video Pipeline")

        for agent in self.agents:

            logger.info(f"Executing {agent.name}")

            result = agent.execute(context)

            if not result.success:

                logger.error(
                    f"{agent.name} failed : {result.error}"
                )

                return result

            context = result.context

        logger.success("Video Pipeline Completed")

        return result