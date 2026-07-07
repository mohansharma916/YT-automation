import json
from pathlib import Path

from app.models.metadata import Metadata


class MetadataService:

    def __init__(self):

        self.output = Path("metadata")

        self.output.mkdir(
            parents=True,
            exist_ok=True,
        )

    ####################################################
    # Save Complete Metadata
    ####################################################

    def save(
        self,
        metadata: Metadata,
    ):

        output = self.output / "metadata.json"

        output.write_text(

            json.dumps(

                metadata.model_dump(),

                indent=4,

                ensure_ascii=False,

            ),

            encoding="utf-8",

        )

        ####################################################
        # Long Videos
        ####################################################

        long_dir = self.output / "longs"

        long_dir.mkdir(
            exist_ok=True,
        )

        for item in metadata.long_videos:

            (long_dir / f"part_{item.part}.json").write_text(

                json.dumps(

                    item.model_dump(),

                    indent=4,

                    ensure_ascii=False,

                ),

                encoding="utf-8",

            )

        ####################################################
        # Shorts
        ####################################################

        short_dir = self.output / "shorts"

        short_dir.mkdir(
            exist_ok=True,
        )

        for item in metadata.shorts:

            (short_dir / f"short_{item.index}.json").write_text(

                json.dumps(

                    item.model_dump(),

                    indent=4,

                    ensure_ascii=False,

                ),

                encoding="utf-8",

            )