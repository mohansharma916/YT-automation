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

    ####################################################
    # Common Renderer
    ####################################################

    def render_clip(
        self,
        context: JobContext,
        start: float,
        end: float,
        output_video: Path,
        subtitle_file: Path,
        vertical: bool,
    ):

        subtitle = self.subtitle.cut(
            subtitle=context.subtitle,
            start=start,
            end=end,
        )

        subtitle = self.subtitle.normalize(
            subtitle,
        )

        self.subtitle.export_ass(
            subtitle,
            subtitle_file,
        )

        self.ffmpeg.render_video(
            background_video=context.background_video,
            podcast_audio=context.local_audio,
            subtitle_file=subtitle_file,
            output_file=output_video,
            start=start,
            end=end,
            vertical=vertical,
        )

    ####################################################
    # Execute
    ####################################################

    def execute(
        self,
        context: JobContext,
    ):

        self.log_start()

        long_dir = Path("output/longs")
        short_dir = Path("output/shorts")

        long_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        short_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        context.output_long_videos = []
        context.output_short_videos = []

        ####################################################
        # Long Videos
        ####################################################

        total = len(
            context.video_parts.parts,
        )

        for part in context.video_parts.parts:

            print(
                f"\nRendering Long {part.part}/{total}"
            )

            subtitle_file = (
                long_dir /
                f"part_{part.part}.ass"
            )

            output_video = (
                long_dir /
                f"Part_{part.part}.mp4"
            )

            self.render_clip(
                context=context,
                start=part.start,
                end=part.end,
                output_video=output_video,
                subtitle_file=subtitle_file,
                vertical=False,
            )

            context.output_long_videos.append(
                output_video,
            )

            print(
                f"✅ Long Part {part.part} Completed"
            )

        ####################################################
        # Shorts
        ####################################################

        print("\nGenerating Shorts...\n")

        for index, short in enumerate(
            context.shorts.shorts,
            start=1,
        ):

            print(
                f"Rendering Short {index}"
            )

            subtitle_file = (
                short_dir /
                f"short_{index}.ass"
            )

            output_video = (
                short_dir /
                f"Short_{index}.mp4"
            )

            self.render_clip(
                context=context,
                start=short.start,
                end=short.end,
                output_video=output_video,
                subtitle_file=subtitle_file,
                vertical=True,
            )

            context.output_short_videos.append(
                output_video,
            )

            print(
                f"✅ Short {index} Completed"
            )

        return self.success(
            context,
        )