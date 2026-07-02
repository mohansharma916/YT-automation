from pathlib import Path
import subprocess


class FFmpegTimelineService:

    def cut_audio(
        self,
        input_audio: Path,
        start: float,
        end: float,
        output: Path,
    ):

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(input_audio),
                "-ss",
                str(start),
                "-to",
                str(end),
                "-c",
                "copy",
                str(output),
            ],
            check=True,
        )

        return output

    def concat_audio(
        self,
        audios: list[Path],
        output: Path,
    ):

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        concat = output.parent / "concat.txt"

        concat.write_text(
            "\n".join(
                f"file '{audio.resolve()}'"
                for audio in audios
            )
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

    def cut_video(
        self,
        input_video: Path,
        start: float,
        end: float,
        output: Path,
    ):

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(input_video),
                "-ss",
                str(start),
                "-to",
                str(end),
                "-c",
                "copy",
                str(output),
            ],
            check=True,
        )

        return output

    def concat_video(
        self,
        videos: list[Path],
        output: Path,
    ):

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        concat = output.parent / "concat.txt"

        concat.write_text(
            "\n".join(
                f"file '{video.resolve()}'"
                for video in videos
            )
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