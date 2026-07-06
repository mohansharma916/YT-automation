from pathlib import Path

import gdown


class DriveService:

    def __init__(self):

        self.download_dir = Path("downloads/audio")

        self.download_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    ####################################################
    # Download
    ####################################################

    def download(
        self,
        audio: str,
    ) -> Path:

        ####################################################
        # Local File
        ####################################################

        local = Path("audio") / audio

        if local.exists():

            print(f"Using Local Audio : {local}")

            return local

        ####################################################
        # Google Drive URL
        ####################################################

        if audio.startswith("http"):

            return self.download_google_drive(
                audio,
            )

        raise FileNotFoundError(
            f"Audio not found : {audio}"
        )

    ####################################################
    # Google Drive
    ####################################################

    def download_google_drive(
        self,
        url: str,
    ) -> Path:

        file_id = self.extract_file_id(
            url,
        )

        output = (
            self.download_dir
            / f"{file_id}.wav"
        )

        if output.exists():

            print(
                f"Already Downloaded : {output}"
            )

            return output

        print("Downloading Audio...")

        gdown.download(
            id=file_id,
            output=str(output),
            fuzzy=True,
            quiet=False,
        )

        return output

    ####################################################
    # File Id
    ####################################################

    def extract_file_id(
        self,
        url: str,
    ) -> str:

        if "/file/d/" in url:

            return (
                url
                .split("/file/d/")[1]
                .split("/")[0]
            )

        if "id=" in url:

            return (
                url
                .split("id=")[1]
                .split("&")[0]
            )

        raise ValueError(
            "Invalid Google Drive URL"
        )