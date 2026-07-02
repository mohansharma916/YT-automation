from pathlib import Path

from app.models.short import Shorts
from app.models.subtitle import Subtitle
from app.models.transcript import Transcript
from app.models.hook import ViralHook


class AIProvider:

    def transcribe(
        self,
        audio_path: Path,
    ) -> Transcript:
        raise NotImplementedError()
    
    def find_hook(self, subtitle) -> ViralHook:
        raise NotImplementedError()

    def generate_subtitles(
        self,
        transcript: Transcript,
    ) -> Subtitle:
        raise NotImplementedError()
    
    def generate_shorts(
    self,
    subtitle,
) -> Shorts:
        raise NotImplementedError()