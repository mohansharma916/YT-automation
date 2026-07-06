from pathlib import Path

from app.agents.base_agent import BaseAgent
from app.models.job_context import JobContext
from app.services.ffmpeg_service import FFmpegService
from app.services.subtitle_service import SubtitleService


class RenderAgent(BaseAgent):

    name = "RenderAgent"

    def __init__(self):

        self.ffmpeg = FFmpegService()
        self.subtitle = SubtitleService()

    def execute(
        self,
        context: JobContext,
    ):

        self.log_start()

        output_dir = Path("output")

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        context.output_long_videos = []

        total_parts = len(
            context.video_parts.parts,
        )

        ####################################################
        # Render Each Part
        ####################################################

        for part in context.video_parts.parts:

            print(
                f"\nRendering Part {part.part}/{total_parts}"
            )

            ####################################################
            # Subtitle
            ####################################################

            subtitle = self.subtitle.cut(
                subtitle=context.subtitle,
                start=part.start,
                end=part.end,
            )

            subtitle = self.subtitle.normalize(
                subtitle,
            )

            subtitle_file = (
                output_dir
                / f"part_{part.part}.ass"
            )

            self.subtitle.export_ass(
                subtitle,
                subtitle_file,
            )

            ####################################################
            # Output
            ####################################################

            output_video = (
                output_dir
                / f"Part_{part.part}.mp4"
            )

            ####################################################
            # Render
            ####################################################

            self.ffmpeg.render_video(

                background_video=context.background_video,

                podcast_audio=context.local_audio,

                subtitle_file=subtitle_file,

                output_file=output_video,

                start=part.start,

                end=part.end,

                vertical=False,

            )

            context.output_long_videos.append(
                output_video,
            )

            print(
                f"✅ Part {part.part} Completed"
            )

        return self.success(
            context,
        )