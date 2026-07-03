import json
from pathlib import Path

from app.models.metadata import Metadata


class MetadataService:
    def save(
        self,
        metadata: Metadata,
    ):

        long_dir = Path("output/long")

        long_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        (long_dir / "metadata.json").write_text(
            json.dumps(
                metadata.long_video.model_dump(),
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        for index, short in enumerate(
            metadata.shorts,
            start=1,
        ):
            folder = Path("output/shorts") / f"short_{index}"

            folder.mkdir(
                parents=True,
                exist_ok=True,
            )

            (folder / "metadata.json").write_text(
                json.dumps(
                    short.model_dump(),
                    indent=4,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
