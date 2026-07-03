import subprocess
from pathlib import Path


class FFmpegService:

    def _run(self, command: list[str]):

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print(result.stderr)
            raise RuntimeError(result.stderr)

    ########################################################
    # Video
    ########################################################

    def get_duration(
        self,
        media_path: Path,
    ) -> float:

        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(media_path),
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        return float(result.stdout.strip())

    def loop_video(
        self,
        video_path: Path,
        duration: float,
        output_path: Path,
    ):

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._run(
            [
                "ffmpeg",
                "-y",
                "-stream_loop",
                "-1",
                "-i",
                str(video_path),
                "-t",
                str(duration),
                "-an",
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                str(output_path),
            ]
        )

        return output_path

    def cut_video(
        self,
        video_path: Path,
        start: float,
        end: float,
        output_path: Path,
    ):

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._run(
            [
                "ffmpeg",
                "-y",
                "-ss",
                str(start),
                "-to",
                str(end),
                "-i",
                str(video_path),
                "-c:v",
                "libx264",
                "-c:a",
                "copy",
                str(output_path),
            ]
        )

        return output_path

    def crop_to_vertical(
        self,
        video_path: Path,
        output_path: Path,
    ):

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(video_path),
                "-vf",
                "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
                "-c:v",
                "libx264",
                "-c:a",
                "copy",
                str(output_path),
            ]
        )

        return output_path

    ########################################################
    # Audio
    ########################################################

    def cut_audio(
        self,
        audio_path: Path,
        start: float,
        end: float,
        output_path: Path,
    ):

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._run(
            [
                "ffmpeg",
                "-y",
                "-ss",
                str(start),
                "-to",
                str(end),
                "-i",
                str(audio_path),
                "-c",
                "copy",
                str(output_path),
            ]
        )

        return output_path

    def concat_audio(
        self,
        audio_files: list[Path],
        output_path: Path,
    ):

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        concat = output_path.parent / "audio_concat.txt"

        concat.write_text(
            "\n".join(
                f"file '{file.resolve()}'"
                for file in audio_files
            )
        )

        self._run(
            [
                "ffmpeg",
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat),
                "-c:a",
                "pcm_s16le",
                str(output_path),
            ]
        )

        concat.unlink(missing_ok=True)

        return output_path

    ########################################################
    # Render
    ########################################################

    def replace_audio(
        self,
        video_path: Path,
        audio_path: Path,
        output_path: Path,
    ):

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(video_path),
                "-i",
                str(audio_path),
                "-map",
                "0:v:0",
                "-map",
                "1:a:0",
                "-c:v",
                "copy",
                "-c:a",
                "aac",
                "-shortest",
                "-movflags",
                "+faststart",
                str(output_path),
            ]
        )

        return output_path

    def burn_subtitles(
        self,
        video_path: Path,
        subtitle_path: Path,
        output_path: Path,
    ):

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(video_path),
                "-vf",
                f"ass={subtitle_path}",
                "-c:a",
                "copy",
                str(output_path),
            ]
        )

        return output_path