from abc import ABC
from abc import abstractmethod

from pathlib import Path

from app.models.subtitle import Subtitle


class TranscriptionProvider(ABC):

    @abstractmethod
    def transcribe(
        self,
        audio_path: Path,
    ) -> Subtitle:
        pass