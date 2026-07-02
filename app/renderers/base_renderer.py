from abc import ABC, abstractmethod
from pathlib import Path

from app.models.subtitle import Subtitle


class BaseSubtitleRenderer(ABC):

    @abstractmethod
    def render(
        self,
        subtitle: Subtitle,
        output_file: Path,
    ):
        pass