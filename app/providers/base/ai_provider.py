from pathlib import Path

from app.models.metadata import Metadata
from app.models.short import Shorts
from app.models.subtitle import Subtitle
from app.models.transcript import Transcript

class AIProvider:

    def transcribe(
        self,
        audio_path: Path,
    ) -> Transcript:
        raise NotImplementedError()
    

    def generate_subtitles(
        self,
        transcript: Transcript,
    ) -> Subtitle:
        raise NotImplementedError()
    
    def generate_metadata(
    self,
    subtitle,
    shorts,
) -> Metadata:
       raise NotImplementedError()
    
    def generate_shorts(
    self,
    subtitle,
) -> Shorts:
        raise NotImplementedError()