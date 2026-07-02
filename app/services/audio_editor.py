from pathlib import Path
import subprocess


class AudioEditor:

    def create_hook_audio(
        self,
        audio_path: Path,
        start: float,
        end: float,
        output: Path,
    ):

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        hook_audio = output.parent / "hook.wav"

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(audio_path),
                "-ss",
                str(start),
                "-to",
                str(end),
                str(hook_audio),
            ],
            check=True,
        )

        concat = output.parent / "concat.txt"

        concat.write_text(
            f"file '{hook_audio.resolve()}'\n"
            f"file '{audio_path.resolve()}'\n"
        )

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat),
                "-c",
                "copy",
                str(output),
            ],
            check=True,
        )

        return output