from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from google_auth_oauthlib.flow import InstalledAppFlow

from googleapiclient.discovery import build

from googleapiclient.http import MediaFileUpload


SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload"
]


class YoutubeService:

    def __init__(self):

        creds = None

        if Path("token.json").exists():

            creds = Credentials.from_authorized_user_file(
                "token.json",
                SCOPES,
            )

        if not creds or not creds.valid:

            if creds and creds.expired and creds.refresh_token:

                creds.refresh(Request())

            else:

                flow = InstalledAppFlow.from_client_secrets_file(
                    "client_secret.json",
                    SCOPES,
                )

                creds = flow.run_local_server(port=0)

            Path("token.json").write_text(
                creds.to_json()
            )

        self.youtube = build(
            "youtube",
            "v3",
            credentials=creds,
        )

    def upload(
        self,
        video,
        metadata,
    ):

        body = {

            "snippet": {

                "title": metadata.title,

                "description": metadata.description,

                "tags": metadata.hashtags,

                "categoryId": "22",
            },

            "status": {

                "privacyStatus": "private",

                "selfDeclaredMadeForKids": False,
            },
        }

        request = self.youtube.videos().insert(

            part="snippet,status",

            body=body,

            media_body=MediaFileUpload(
                str(video),
                resumable=True,
            ),
        )

        response = None

        while response is None:

            _, response = request.next_chunk()

        return response["id"]