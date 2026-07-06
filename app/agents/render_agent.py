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

        ####################################################
        # Subtitle
        ####################################################

        subtitle = self.subtitle.cut(
            subtitle=context.subtitle,
            start=start,
            end=end,
        )

        subtitle = self.subtitle.normalize(
            subtitle,
        )

        self.subtitle.export_ass(
            subtitle=subtitle,
            output_file=subtitle_file,
            vertical=vertical,
        )

        ####################################################
        # Render
        ####################################################

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

        ####################################################
        # Folders
        ####################################################

        long_dir = Path("output/longs")
        short_dir = Path("output/shorts")
        subtitle_dir = Path("output/subtitles")

        long_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        short_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        subtitle_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        ####################################################
        # Reset Outputs
        ####################################################

        context.output_long_videos = []
        context.output_short_videos = []

        ####################################################
        # Long Videos
        ####################################################

        total_parts = len(
            context.video_parts.parts,
        )

        print("\n")
        print("=" * 70)
        print("Generating Long Videos")
        print("=" * 70)

        for part in context.video_parts.parts:

            print(
                f"\nRendering Long Video {part.part}/{total_parts}"
            )

            subtitle_file = (
                subtitle_dir
                / f"part_{part.part}.ass"
            )

            output_video = (
                long_dir
                / f"Part_{part.part}.mp4"
            )

            print("=" * 50)
            print("Rendering LONG")
            print("Vertical=False")
            print(output_video)
            print("=" * 50)

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
                f"✅ Part {part.part} Completed"
            )

        ####################################################
        # Shorts
        ####################################################

        if (
            context.shorts
            and len(context.shorts.shorts) > 0
        ):

            print("\n")
            print("=" * 70)
            print("Generating Shorts")
            print("=" * 70)

            for index, short in enumerate(
                context.shorts.shorts,
                start=1,
            ):

                print(
                    f"\nRendering Short {index}/{len(context.shorts.shorts)}"
                )

                subtitle_file = (
                    subtitle_dir
                    / f"short_{index}.ass"
                )

                output_video = (
                    short_dir
                    / f"Short_{index}.mp4"
                )


                print("=" * 50)
                print("Rendering SHORT")
                print("Vertical=True")
                print(short.start, short.end)
                print("=" * 50)

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

        ####################################################
        # Summary
        ####################################################

        print("\n")
        print("=" * 70)
        print("Rendering Completed")
        print("=" * 70)

        print(
            f"Long Videos : {len(context.output_long_videos)}"
        )

        print(
            f"Short Videos : {len(context.output_short_videos)}"
        )

        print("=" * 70)

        return self.success(
            context,
        )