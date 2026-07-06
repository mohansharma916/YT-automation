import json
from pathlib import Path

from yt_dlp import YoutubeDL
from yt_dlp.utils import download_range_func


class YoutubeService:

    def __init__(self):

     

    
   

        self.output = Path(
            "downloads/background"
        )

        self.output.mkdir(
            parents=True,
            exist_ok=True,
        )

    ####################################################
    # Download Background Video
    ####################################################

    def download_background_video(
        self,
        url: str,
        duration: float,
    ) -> Path:

        

        options = {

            "format": "bestvideo+bestaudio/best",

            "merge_output_format": "mp4",

            "outtmpl": str(
                self.output / "%(id)s.%(ext)s"
            ),

            "download_ranges": download_range_func(
                None,
                [
                    (
                        0,
                        duration,
                    )
                ],
            ),

            "force_keyframes_at_cuts": True,
        }

        with YoutubeDL(options) as ydl:

            info = ydl.extract_info(
                url,
                download=True,
            )

            return Path(
                ydl.prepare_filename(
                    info,
                )
            ).with_suffix(".mp4")