from app.agents.base_agent import BaseAgent
from app.models.job_context import JobContext
from app.providers.factory.provider_factory import ProviderFactory
from app.services.subtitle_service import SubtitleService
from app.services.metadata_service import MetadataService

class MetadataAgent(BaseAgent):

    name = "MetadataAgent"

    def __init__(self):

        self.provider = ProviderFactory.llm()
        self.subtitle = SubtitleService()
        self.metadata_service = MetadataService()

    ####################################################
    # Execute
    ####################################################

    def execute(
        self,
        context: JobContext,
    ):

        self.log_start()

        ####################################################
        # Long Video Subtitles
        ####################################################

        long_subtitles = []

        for part in context.video_parts.parts:

            subtitle = self.subtitle.cut(
                subtitle=context.subtitle,
                start=part.start,
                end=part.end,
            )

            subtitle = self.subtitle.normalize(
                subtitle,
            )

            long_subtitles.append(
                subtitle,
            )

        ####################################################
        # Shorts Subtitles
        ####################################################

        short_subtitles = []

        for short in context.shorts.shorts:

            subtitle = self.subtitle.cut(
                subtitle=context.subtitle,
                start=short.start,
                end=short.end,
            )

            subtitle = self.subtitle.normalize(
                subtitle,
            )

            short_subtitles.append(
                subtitle,
            )

        ####################################################
        # AI
        ####################################################

        metadata = self.provider.generate_metadata(
            long_subtitles=long_subtitles,
            short_subtitles=short_subtitles,
        )

        ####################################################
        # Inject Timeline
        ####################################################

        for item, part in zip(
            metadata.long_videos,
            context.video_parts.parts,
        ):

            item.part = part.part
            item.start = part.start
            item.end = part.end

        for index, (item, short) in enumerate(zip(metadata.shorts, context.shorts.shorts),start=1,) :

            item.index = index
            item.start = short.start
            item.end = short.end

        ####################################################
        # Save
        ####################################################

        context.metadata_ai = metadata
        self.metadata_service.save(metadata)

        return self.success(
            context,
        )