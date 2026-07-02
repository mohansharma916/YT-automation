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

        if context.hook is None:
            raise ValueError("Hook not found.")

        if context.shorts is None:
            raise ValueError("Shorts not found.")

        if context.subtitle is None:
            raise ValueError("Subtitle not found.")

        if context.local_audio is None:
            raise ValueError("Audio not found.")

        if context.downloaded_video is None:
            raise ValueError("Background video not found.")

        long_dir = Path("output/long")
        shorts_dir = Path("output/shorts")

        long_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        shorts_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        ####################################################
        # LONG VIDEO
        ####################################################

        print("\nCreating Long Video...\n")

        hook_audio = long_dir / "audio.wav"

        self.ffmpeg.create_hook_audio(
            audio_path=context.local_audio,
            hook_start=context.hook.start,
            hook_end=context.hook.end,
            output_path=hook_audio,
        )

        hook_subtitle = self.subtitle.create_hook_subtitle(
            subtitle=context.subtitle,
            hook_start=context.hook.start,
            hook_end=context.hook.end,
        )

        hook_ass = long_dir / "subtitle.ass"

        self.subtitle.save_ass(
            hook_subtitle,
            hook_ass,
        )

        temp_video = long_dir / "temp.mp4"

        self.ffmpeg.replace_audio(
            video_path=context.downloaded_video,
            audio_path=hook_audio,
            output_path=temp_video,
        )

        final_video = long_dir / "final.mp4"

        self.ffmpeg.burn_subtitles(
            video_path=temp_video,
            subtitle_path=hook_ass,
            output_path=final_video,
        )

        context.output_video = final_video

        ####################################################
        # SHORTS
        ####################################################

        print("\nCreating Shorts...\n")

        for index, short in enumerate(
            context.shorts.shorts,
            start=1,
        ):

            print(
                f"Creating Short {index} ({short.start} - {short.end})"
            )

            short_dir = shorts_dir / f"short_{index}"

            short_dir.mkdir(
                parents=True,
                exist_ok=True,
            )

            ####################################################
            # Audio
            ####################################################

            short_audio = short_dir / "audio.wav"

            self.ffmpeg.cut_audio(
                audio_path=context.local_audio,
                start=short.start,
                end=short.end,
                output_path=short_audio,
            )

            ####################################################
            # Subtitle
            ####################################################

            short_subtitle = self.subtitle.cut(
                subtitle=context.subtitle,
                start=short.start,
                end=short.end,
            )

            short_subtitle = self.subtitle.normalize(
                short_subtitle,
            )

            short_ass = short_dir / "subtitle.ass"

            self.subtitle.save_ass(
                short_subtitle,
                short_ass,
            )

            ####################################################
            # Background Video
            ####################################################

            short_video = short_dir / "background.mp4"

            self.ffmpeg.cut_video(
                video_path=context.downloaded_video,
                start=0,
                end=short.end - short.start,
                output_path=short_video,
            )

            ####################################################
            # Replace Audio
            ####################################################

            temp_video = short_dir / "temp.mp4"

            self.ffmpeg.replace_audio(
                video_path=short_video,
                audio_path=short_audio,
                output_path=temp_video,
            )

            ####################################################
            # Burn Subtitle
            ####################################################

            self.ffmpeg.burn_subtitles(
                video_path=temp_video,
                subtitle_path=short_ass,
                output_path=short_dir / "video.mp4",
            )

      
        print("\n✅ Rendering Completed\n")
        return self.success(context)