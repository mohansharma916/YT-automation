from pathlib import Path
import subprocess

from app.models.short import Shorts


class ShortsEditor:

    def create(
        self,
        video_path: Path,
        audio_path: Path,
        shorts: Shorts,
        output_dir: Path,
    ):

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        generated = []

        for index, short in enumerate(shorts.shorts, start=1):

            output = output_dir / f"short_{index}.mp4"

            command = [
                "ffmpeg",
                "-y",

                "-stream_loop",
                "-1",

                "-i",
                str(video_path),

                "-i",
                str(audio_path),

                "-ss",
                str(short.start),

                "-to",
                str(short.end),

                "-map",
                "0:v:0",

                "-map",
                "1:a:0",

                "-c:v",
                "copy",

                "-c:a",
                "aac",

                "-shortest",

                str(output),
            ]

            subprocess.run(
                command,
                check=True,
            )

            generated.append(output)

        return generated