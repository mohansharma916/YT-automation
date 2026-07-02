from pathlib import Path

from google import genai

from app.config.settings import settings
from app.models.transcript import Transcript
from app.models.subtitle import Subtitle


class GeminiProvider:

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.gemini_api_key
        )
    
    def generate_subtitles(
    self,
    audio_path: Path) -> Subtitle:

        uploaded_file = self.client.files.upload(
            file=str(audio_path)
        )

        prompt = """
        You are an expert subtitle generation engine.

        Listen carefully to the attached audio.

        Return subtitle segments.

        Rules

        - Preserve the original language.

        - Never translate.

        - Split at natural speech pauses.

        - Keep subtitles comfortably readable.

        - Usually between 4 and 8 words.

        - Estimate timestamps.

        - Return ONLY subtitle data.
        """

        response = self.client.models.generate_content(
        model=settings.gemini_model,

        contents=[
            prompt,
            uploaded_file,
        ],

        config={
            "response_mime_type": "application/json",
            "response_schema": Subtitle,
        },
    )

        return response.parsed

    def transcribe(self, audio_path: Path) -> Transcript:

        uploaded_file = self.client.files.upload(
            file=str(audio_path)
        )

        prompt = """
        You are a transcription assistant.

        Your task is to transcribe the attached audio.

        Rules:
        - Return ONLY the spoken words.
        - Do not summarize.
        - Do not explain.
        - Do not add markdown.
        - Preserve paragraphs where appropriate.
        """

        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    prompt,
                    uploaded_file
                ]
            )
        except Exception as e:
            raise ValueError(f"Error occurred while transcribing audio: {e}")

        return Transcript(
            text=response.text.strip()
        )
        

      