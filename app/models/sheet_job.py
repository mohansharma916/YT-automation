from dataclasses import dataclass


@dataclass
class SheetJob:

    row: int

    job_id: str

    background_video: str

    audio_url: str

    status: str