import subprocess
from pathlib import Path
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
        "-c:v",
        "libx264",

        "-c:a",
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

        concat = output_path.parent / "videos.txt"

        concat.write_text(
        "\n".join(
            [
                f"file '{v.resolve()}'"
                for v in videos
            ]
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
        str(concat),
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


    def crop_to_vertical(
    self,
    video_path: Path,
    output_path: Path):

        output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

        command = [
        "ffmpeg",
        "-y",
        "-i",
        str(video_path),

        "-vf",
        "crop=ih*9/16:ih,scale=1080:1920",

         "-c:v",
        "libx264",

        "-c:a",
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

            "-movflags",
            "+faststart",

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
        

    
    def prepend_video(
    self,
    hook_video: Path,
    full_video: Path,
    output_path: Path):

        output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

        concat_file = output_path.parent / "videos.txt"

        concat_file.write_text(
        "\n".join(
            [
                f"file '{hook_video.resolve()}'",
                f"file '{full_video.resolve()}'",
            ]
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
        
    