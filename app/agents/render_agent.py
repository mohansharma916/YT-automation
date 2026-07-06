from pathlib import Path
from tempfile import TemporaryDirectory

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

        if context.downloaded_video is None:
            raise ValueError("Background video missing.")

        if context.local_audio is None:
            raise ValueError("Audio missing.")

        if context.subtitle is None:
            raise ValueError("Subtitle missing.")

        if context.shorts is None:
            raise ValueError("Shorts missing.")

        output_long = Path("output/long")
        output_short = Path("output/shorts")

        output_long.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_short.mkdir(
            parents=True,
            exist_ok=True,
        )

        with TemporaryDirectory() as temp:

            temp = Path(temp)

            ####################################################
            # LONG VIDEO
            ####################################################

            duration = self.ffmpeg.get_duration(
                context.local_audio,
            )

            loop_video = temp / "loop.mp4"

            self.ffmpeg.loop_video(
                video_path=context.downloaded_video,
                duration=duration,
                output_path=loop_video,
            )

            hook_audio = temp / "hook.wav"

            self.ffmpeg.cut_audio(
                audio_path=context.local_audio,
                start=context.hook.start,
                end=context.hook.end,
                output_path=hook_audio,
            )

            final_audio = temp / "final.wav"

            self.ffmpeg.concat_audio(
                [
                    hook_audio,
                    context.local_audio,
                ],
                final_audio,
            )

            print("INPUT SEGMENTS:", len(context.subtitle.segments))

            final_subtitle = self.subtitle.create_final_subtitle(
                subtitle=context.subtitle,
                hook_start=context.hook.start,
                hook_end=context.hook.end,
            )

            print("FINAL SEGMENTS:", len(final_subtitle.segments))

            subtitle_ass = temp / "subtitle.ass"

            self.subtitle.save_ass(
                final_subtitle,
                subtitle_ass,
            )

            temp_video = temp / "video.mp4"

            self.ffmpeg.replace_audio(
                video_path=loop_video,
                audio_path=final_audio,
                output_path=temp_video,
            )

            final_video = output_long / "final.mp4"

            self.ffmpeg.burn_subtitles(
                video_path=temp_video,
                subtitle_path=subtitle_ass,
                output_path=final_video,
            )

            context.output_video = final_video

            ####################################################
            # SHORTS
            ####################################################

            for index, short in enumerate(
                context.shorts.shorts,
                start=1,
            ):

                short_duration = (
                    short.end - short.start
                )

                short_loop = temp / f"loop_{index}.mp4"

                self.ffmpeg.loop_video(
                    video_path=context.downloaded_video,
                    duration=short_duration,
                    output_path=short_loop,
                )

                vertical_video = temp / f"vertical_{index}.mp4"

                self.ffmpeg.crop_to_vertical(
                    video_path=short_loop,
                    output_path=vertical_video,
                )

                short_audio = temp / f"audio_{index}.wav"

                self.ffmpeg.cut_audio(
                    audio_path=context.local_audio,
                    start=short.start,
                    end=short.end,
                    output_path=short_audio,
                )

                short_subtitle = self.subtitle.create_short_subtitle(
                    subtitle=context.subtitle,
                    start=short.start,
                    end=short.end,
                )

                short_ass = temp / f"subtitle_{index}.ass"

                self.subtitle.save_ass(
                    short_subtitle,
                    short_ass,
                )

                short_temp = temp / f"temp_{index}.mp4"

                self.ffmpeg.replace_audio(
                    video_path=vertical_video,
                    audio_path=short_audio,
                    output_path=short_temp,
                )

                short_output = (
                    output_short / f"short_{index}.mp4"
                )

                self.ffmpeg.burn_subtitles(
                    video_path=short_temp,
                    subtitle_path=short_ass,
                    output_path=short_output,
                )

                print(
                    f"✅ Short {index} Rendered"
                )

                            ####################################################
            # DONE
            ####################################################

            print("\n====================================")
            print("✅ Long Video Rendered")
            print("✅ Shorts Rendered")
            print("====================================\n")

        return self.success(context)