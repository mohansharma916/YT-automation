import json
from pathlib import Path

from app.models.subtitle_theme import SubtitleTheme


class ThemeService:

    def load(
        self,
        theme_name: str,
    ) -> SubtitleTheme:

        file = Path("themes") / f"{theme_name}.json"

        data = json.loads(
            file.read_text(
                encoding="utf-8"
            )
        )

        return SubtitleTheme(**data)