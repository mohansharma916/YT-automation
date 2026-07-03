import json
import time

import requests
from sarvamai import SarvamAI

from app.config.settings import settings
from app.models.subtitle import Subtitle
from app.models.subtitle import SubtitleSegment
from app.providers.base.transcription_provider import TranscriptionProvider


class SarvamProvider(TranscriptionProvider):

    def __init__(self):

        self.client = SarvamAI(
            api_subscription_key=settings.sarvam_api_key,
        )

    def get_upload_url(
    self,
    job_id: str,
    filename: str):
        

        response = self.client.speech_to_text_job.get_upload_links(
        job_id=job_id,
        files=[filename],
    )

        return response.upload_urls[filename].file_url

    def transcribe(self, audio_path):

        job = self.create_job()

        print("Job Created :", job.job_id)

        upload_url = self.get_upload_url(
            job.job_id,
            audio_path.name,
        )

        self.upload_audio(
            upload_url,
            audio_path,
        )

        self.start_job(
            job.job_id,
        )

        status = self.wait_until_completed(
            job.job_id,
        )

        download_url = self.get_download_url(
            status,
            job.job_id,
        )

        data = requests.get(download_url).json()
        print(json.dumps(data, indent=4, ensure_ascii=False))

        return self.parse(data)


    def upload_audio(
    self,
    upload_url: str,
    audio_path):


        with open(audio_path, "rb") as f:

            response = requests.put(
            upload_url,
            data=f,
            headers={
                "x-ms-blob-type": "BlockBlob",
                "Content-Type": "application/octet-stream",
            },
        )

        print(response.status_code)
        print(response.text)

        response.raise_for_status()


    def start_job(
    self,
    job_id: str):

        self.client.speech_to_text_job.start(
        job_id=job_id,
    )
    

    def wait_until_completed(
    self,
    job_id: str,):

        while True:

            status = self.client.speech_to_text_job.get_status(
            job_id=job_id,
        )

            print(status.job_state)

            if status.job_state == "Completed":
                return status

            if status.job_state == "Failed":
                raise Exception("Sarvam Job Failed")

            time.sleep(5)



    def get_download_url(
    self,
    status,
    job_id):
      

      filename = (
        status.job_details[0]
        .outputs[0]
        .file_name
    )

      response = self.client.speech_to_text_job.get_download_links(
        job_id=job_id,
        files=[filename],
    )

      return response.download_urls[filename].file_url
    



    def parse(
    self,
    data,
):
        

         timestamps = data["timestamps"]

         words = timestamps["words"]
         starts = timestamps["start_time_seconds"]
         ends = timestamps["end_time_seconds"]

         segments = []

         for word, start, end in zip(
        words,
        starts,
        ends,
        ):

          segments.append(

            SubtitleSegment(

                start=float(start),

                end=float(end),

                text=word,

            )

        )

         return Subtitle(
        segments=segments,
    )

    def create_job(self):

        return self.client.speech_to_text_job.initialise(

        job_parameters={

            "model": "saaras:v3",

            "language_code": "hi-IN",

            "mode": "transcribe",

            "with_timestamps": True,

            "with_diarization": False,

        }

    )