from app.agents.base_agent import BaseAgent
from app.models.job_context import JobContext
from app.orchestrator.video_pipeline import VideoPipeline
from app.services.drive_service import DriveService
from app.services.google_sheet_service import GoogleSheetService


class SheetAgent(BaseAgent):

    name = "SheetAgent"

    def __init__(self):

        self.sheet = GoogleSheetService()
        self.drive = DriveService()
        self.pipeline = VideoPipeline()

    ####################################################
    # Execute
    ####################################################

    def execute(
        self,
        sheet_name: str,
    ):

        while True:

            ####################################################
            # Get Pending Job
            ####################################################

            job = self.sheet.get_pending_job(
                sheet_name,
            )
            print(f"\nProcessing Job : {job}\n")
            if job is None:

                print("\nNo Pending Jobs\n")

                break

            print(f"\nProcessing Job : {job.job_id}\n")

            ####################################################
            # Download Audio
            ####################################################

            try:

                self.sheet.update_status(
                    sheet_name,
                    job.row,
                    "DOWNLOADING_AUDIO",
                )

                audio = self.drive.download(
                    job.audio_url,
                )

                ####################################################
                # Context
                ####################################################

                context = JobContext(

                    job_id=job.job_id,

                    sheet_name=sheet_name,

                    sheet_row=job.row,

                    local_audio=audio,

                    background_video_url=job.background_video,

                )

                ####################################################
                # Pipeline
                ####################################################

                result = self.pipeline.run(
                    context,
                )

                ####################################################
                # Success
                ####################################################

                if result.success:

                    self.sheet.update_status(
                        sheet_name,
                        job.row,
                        "COMPLETED",
                    )

                    print(
                        f"\nJob {job.job_id} Completed\n"
                    )

                ####################################################
                # Failed
                ####################################################

                else:

                    self.sheet.update_status(
                        sheet_name,
                        job.row,
                        "FAILED",
                    )

                    self.sheet.update_error(
                        sheet_name,
                        job.row,
                        result.error,
                    )

            except Exception as ex:

                import traceback

                traceback.print_exc()

                self.sheet.update_status(
                    sheet_name,
                    job.row,
                    "FAILED",
                )

                self.sheet.update_error(
                    sheet_name,
                    job.row,
                    str(ex),
                )