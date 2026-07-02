import subprocess
from pathlib import Path
from unittest import result

from click import command


class FFmpegService:

    def burn_subtitles(
        self,
        video_path: Path,
        subtitle_path: Path,
        output_path: Path,):
        output_path.parent.mkdir(
        parents=True,
        exist_ok=True,)

        command = [

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

        print("\nFFmpeg Burn Subtitle Command:\n")
        print(" ".join(command))
        print()

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print(result.stderr)
            raise RuntimeError(result.stderr)

    def get_duration(self, media_path: Path) -> float:
        """
        Returns duration in seconds using ffprobe.
        """

        command = [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(media_path),
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
        )

        return float(result.stdout.strip())
    
    def compose_video(
        self,
        video_path: Path,
        audio_path: Path,
        output_path: Path,
    ):

        self.replace_audio(
            video_path=video_path,
            audio_path=audio_path,
            output_path=output_path,
        )
    
    def cut_audio(
    self,
    audio_path: Path,
    start: float,
    end: float,
    output_path: Path,):

        output_path.parent.mkdir(
        parents=True,
        exist_ok=True,)

        command = [
        "ffmpeg",
        "-y",
        "-i",
        str(audio_path),
        "-ss",
        str(start),
        "-to",
        str(end),
        "-c",
        "copy",
        str(output_path),
    ]

        result = subprocess.run(
        command,
        capture_output=True,
        text=True,
    )

        if result.returncode != 0:
            raise RuntimeError(result.stderr)

        return output_path
    


    def concat_audio(
    self,
    audio_files: list[Path],
    output_path: Path):
        
        output_path.parent.mkdir(
        parents=True,
        exist_ok=True,)

        concat_file = output_path.parent / "concat.txt"

        concat_file.write_text(
        "\n".join(
            f"file '{file.resolve()}'"
            for file in audio_files
        )
    )

        command = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_file),
        "-c",
        "copy",
        str(output_path),
    ]

        result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(result.stderr)

        return output_path
    


    def cut_video(
    self,
    video_path: Path,
    start: float,
    end: float,
    output_path: Path):

        output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

        command = [
        "ffmpeg",
        "-y",
        "-ss",
        str(start),
        "-to",
        str(end),
        "-i",
        str(video_path),
        "-c",
        "copy",
        str(output_path),
    ]

        result = subprocess.run(
        command,
        capture_output=True,
        text=True,
    )

        if result.returncode != 0:
          raise RuntimeError(result.stderr)

        return output_path
    


    def concat_video(
    self,
    videos: list[Path],
    output_path: Path):

        output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

        concat_file = output_path.parent / "videos.txt"

        concat_file.write_text(
        "\n".join(
            f"file '{video.resolve()}'"
            for video in videos
        )
    )

        command = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_file),
        "-c",
        "copy",
        str(output_path),
    ]

        result = subprocess.run(
        command,
        capture_output=True,
        text=True,
    )

        if result.returncode != 0:
            raise RuntimeError(result.stderr)

        return output_path


    def create_hook_audio(
    self,
    audio_path: Path,
    hook_start: float,
    hook_end: float,
    output_path: Path):

        hook_audio = output_path.parent / "hook.wav"

        self.cut_audio(
        audio_path,
        hook_start,
        hook_end,
        hook_audio,
        )

        self.concat_audio(
        [
            hook_audio,
            audio_path,
        ],
        output_path,
    )

        return output_path





    def replace_audio(self,video_path: Path,
                            audio_path: Path,
                            output_path: Path):
        """
        Replace the video's audio with the supplied audio.
        """

        command = [
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
            "-c:v","copy",

            "-c:a",
            "aac",

            "-shortest",

            str(output_path),
        ]
        print("\nFFmpeg Command:")
        print(" ".join(command))
        print()

        result = subprocess.run(command,capture_output=True,text=True,)

        print(result.stdout)
        print(result.stderr)

        if result.returncode != 0:
            raise RuntimeError(result.stderr)
        
    