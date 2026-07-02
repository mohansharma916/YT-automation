from multiprocessing import context
from pathlib import Path

from app.models.job_context import JobContext
from app.orchestrator.video_pipeline import VideoPipeline
from app.services.ffmpeg_service import FFmpegService
from app.renderers.ass_renderer import ASSRenderer


def main():

    context = JobContext(
        youtube_url="https://www.youtube.com/watch?v=aYIq2efHS94",
        local_audio=Path("audio/sample.wav"),
    )

    pipeline = VideoPipeline()
    service = FFmpegService()
    renderer = ASSRenderer()

    result = pipeline.run(context)

    if result.success:

        print("\nPipeline Completed Successfully\n")
        print("\n========== VIRAL HOOK ==========\n")

        print(context.hook)

        print("\n========== SHORTS ==========\n")

        for short in context.shorts.shorts:

            print(short)


        print(result.context)
        print(service.get_duration(context.local_audio))
        print(service.replace_audio(
                    video_path=context.downloaded_video,
                    audio_path=context.local_audio,
                    output_path=Path("output/test.mp4"),
))
        print(context.subtitle)
        renderer.render(
    context.subtitle,
    Path("subtitles/sample.ass"),
)


    else:

        print("\nPipeline Failed\n")
        print(result.error)


if __name__ == "__main__":
    main()