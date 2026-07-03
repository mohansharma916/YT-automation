import json


from openai import OpenAI
from app.config.settings import settings
from app.models.metadata import Metadata
from app.models.short import Shorts
from app.models.subtitle import Subtitle, SubtitleSegment
from app.models.transcript import Transcript
from app.providers.base.ai_provider import AIProvider
from app.models.hook import ViralHook


class OpenAIProvider(AIProvider):
    def __init__(self):

        self.client = OpenAI(api_key=settings.openai_api_key)

    def transcribe(self, audio_path):

        with open(audio_path, "rb") as audio:
            response = self.client.audio.transcriptions.create(
                model=settings.transcription_model,
                file=audio,
                response_format="verbose_json",
                timestamp_granularities=["segment"],
            )

        subtitle = Subtitle(
            segments=[
                SubtitleSegment(
                    start=segment.start,
                    end=segment.end,
                    text=segment.text,
                )
                for segment in response.segments
            ]
        )

        return subtitle

    def generate_subtitles(
        self,
        transcript: Transcript,
    ) -> Subtitle:

        prompt = f"""
You are an expert subtitle editor.

Split the following transcript into subtitles.

Rules:

- Maximum 7 words per subtitle.
- Keep natural sentence flow.
- Don't change wording.
- Don't summarize.
- Return ONLY valid JSON.

Format:

{{
    "segments":[
        {{
            "text":"..."
        }}
    ]
}}

Transcript:

{transcript.text}
"""

        response = self.client.responses.create(
            model=settings.chat_model,
            input=prompt,
        )

        content = response.output_text
        print("========== OpenAI Response ==========")
        if content.startswith("```"):
            content = content.replace("```json", "").replace("```", "").strip()

            data = json.loads(content)

            return Subtitle.model_validate(data)

    def find_hook(self, subtitle: Subtitle) -> ViralHook:

        subtitle_json = json.dumps(
            subtitle.model_dump(),
            ensure_ascii=False,
            indent=2,
        )

        prompt = f"""
You are an expert viral content editor.

Below is a subtitle JSON with timestamps.

Find the SINGLE most viral hook.

Rules:

- Pick only ONE.
- It should create maximum curiosity.
- Prefer emotional or shocking moments.
- Hook duration should be between 5 and 12 seconds.
- Return ONLY JSON.

Format:

{{
    "start": 0.0,
    "end": 0.0,
    "hook": "...",
    "reason": "...",
    "score": 95
}}

Subtitle:

{subtitle_json}
        """

        response = self.client.responses.create(
            model=settings.chat_model,
            input=prompt,
        )

        content = response.output_text.strip()

        if content.startswith("```"):
            content = content.replace("```json", "").replace("```", "").strip()

        data = json.loads(content)

        return ViralHook.model_validate(data)

    def generate_metadata(
        self,
        subtitle: Subtitle,
        shorts: Shorts,
    ) -> Metadata:
        subtitle_json = json.dumps(subtitle.model_dump(), ensure_ascii=False, indent=2)
        shorts_json = json.dumps(
            shorts.model_dump(),
            ensure_ascii=False,
            indent=2,
        )

        prompt = f"""
        You are an expert YouTube SEO specialist.

        Generate metadata for:

        1. Long YouTube Video
        2. Every Short.

        Rules:

        - High CTR title
        - SEO optimized description
        - 10 relevant hashtags
        - Return ONLY JSON

        Format:

        {{
            "long_video": {{
                "title": "...",
                "description": "...",
                "hashtags": []
            }},
            "shorts": [
                {{
                    "title": "...",
                    "description": "...",
                    "hashtags": []
                }}
            ]
        }}

        Subtitle:

        {subtitle_json}

        Shorts:

        {shorts_json}
        """

        response = self.client.responses.create(
            model=settings.chat_model,
            input=prompt,
        )

        content = response.output_text.strip()

        if content.startswith("```"):
            content = content.replace("```json", "").replace("```", "").strip()

        data = json.loads(content)

        return Metadata.model_validate(data)

    def generate_shorts(
        self,
        subtitle: Subtitle,
    ) -> Shorts:

        subtitle_json = json.dumps(
            subtitle.model_dump(),
            ensure_ascii=False,
            indent=2,
        )

        prompt = f"""
You are an expert YouTube Shorts editor.

Below is subtitle JSON with timestamps.

Split it into multiple Shorts.

Rules:

- Each short must be under 120 seconds.
- Split only at natural story boundaries.
- Never cut in the middle of a conversation.
- Every short should have a curiosity ending if possible.
- Return ONLY JSON.

Format:

{{
    "shorts":[
        {{
            "title":"...",
            "start":0.0,
            "end":80.0,
            "reason":"..."
        }}
    ]
}}

Subtitle JSON:

{subtitle_json}
"""

        response = self.client.responses.create(
            model=settings.chat_model,
            input=prompt,
        )

        content = response.output_text.strip()

        if content.startswith("```"):
            content = content.replace("```json", "").replace("```", "").strip()

        data = json.loads(content)

        return Shorts.model_validate(data)
