from pathlib import Path

from app.models.job_context import JobContext
from app.orchestrator.video_pipeline import VideoPipeline


def main():

    context = JobContext(
        youtube_url="https://www.youtube.com/watch?v=aYIq2efHS94",
    )

    pipeline = VideoPipeline()

    result = pipeline.run(context)

    if result.success:

        print("\n✅ Pipeline Completed Successfully\n")

    else:

        print("\n❌ Pipeline Failed\n")

        print(result.error)


if __name__ == "__main__":
    main()