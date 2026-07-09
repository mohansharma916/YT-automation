from pathlib import Path
from openai import OpenAI
from rich import json
from app.config.settings import settings
from app.models.subtitle import Subtitle
from app.models.subtitle import SubtitleSegment
from app.providers.base.transcription_provider import (
    TranscriptionProvider,
)


class OpenAITranscriptionProvider(TranscriptionProvider):

    def __init__(self):

        self.client = OpenAI(
            api_key=settings.openai_api_key,
        )

    ####################################################
    # Transcribe
    ####################################################

    def transcribe(
        self,
        audio_path: Path,
    ) -> Subtitle:

        with open(audio_path, "rb") as audio:

            response = self.client.audio.transcriptions.create(

                model="whisper-1",

                file=audio,

                language="hi",

                response_format="verbose_json",

                timestamp_granularities=["segment"],

            )

        segments = []

        for segment in response.segments:

            text = segment.text.strip()

            if not text:
                continue

            segments.append(

                SubtitleSegment(

                    start=float(segment.start),

                    end=float(segment.end),

                    text=text,

                )

            )

        return Subtitle(
            segments=segments,
        )
    



    def correct_subtitles(
    self,
    subtitle: Subtitle) -> Subtitle:
        

        subtitle_json = json.dumps(
        subtitle.model_dump(),
        ensure_ascii=False,
        indent=2)

        prompt = f"""
        You are an expert editor for Indian Hindi and Hinglish call recordings .

        Your job is to improve Whisper subtitles.


        Rules

        - Keep EXACTLY the same number of subtitle segments.
        - Never merge subtitles.
        - Never split subtitles.
        - Never change timestamps.
        - Never invent new sentences.
        - Preserve the meaning.
        - Correct Hindi spelling.
        - Correct Hinglish words if obvious.
        - Add natural punctuation.
        - Keep names unchanged.

        Return ONLY JSON.

        Format

        {{
            "segments":[
                {{
                    "text":"..."
                }}
            ]
        }}

        Subtitle JSON

        {subtitle_json}
        """

        response = self.client.responses.create(

        model=settings.chat_model,

        input=prompt,

    )

        content = response.output_text.strip()

        if content.startswith("```"):

         content = (
            content
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        data = json.loads(content)

    ####################################################
    # Preserve timestamps
    ####################################################

        corrected = []

        for original, item in zip(
        subtitle.segments,
        data["segments"],):

            corrected.append(

            SubtitleSegment(

                start=original.start,

                end=original.end,

                text=item["text"].strip(),

            )

        )

        return Subtitle(
        segments=corrected,
    )