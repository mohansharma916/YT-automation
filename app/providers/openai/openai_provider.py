import json


from openai import OpenAI
from app.config.settings import settings
from app.models.metadata import Metadata
from app.models.short import Shorts
from app.models.subtitle import Subtitle, SubtitleSegment
from app.models.transcript import Transcript
from app.providers.base.ai_provider import AIProvider


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

 

    def subtitle_to_text(
    self,
    subtitle: Subtitle,):
        

     return "\n".join(

        segment.text

        for segment in subtitle.segments

    )


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
    
    def generate_metadata(
    self,
    long_subtitles: list[Subtitle],
    short_subtitles: list[Subtitle],
) -> Metadata:

    ####################################################
    # Build Prompt
    ####################################################

        long_text = []

        for index, subtitle in enumerate(
            long_subtitles,
            start=1,):

            long_text.append(
            f"""
            PART {index}
            {self.subtitle_to_text(subtitle)}
            """
        )

        short_text = []

        for index, subtitle in enumerate(
        short_subtitles,
        start=1,):

            short_text.append(

            f"""
            SHORT {index}

            {self.subtitle_to_text(subtitle)}
            """
        )

        prompt = f"""
        You are one of the world's best YouTube SEO strategists.

        You are given multiple LONG videos and multiple SHORT videos
        generated from the same podcast.

        Generate UNIQUE metadata for EACH ONE.

        Rules

    • Every Long title MUST be completely different.
    • Every Short title MUST be completely different.
    • Never repeat wording.
    • Focus only on that clip.
    • Long titles must end with "| Part X".
    • Maximum title length: 95 characters.
    • Description should be SEO friendly.
    • Generate 15 hashtags.
    • Generate 15 tags.
    • Generate Thumbnail Text.
    • Generate Thumbnail Prompt.
    • Generate Hook Text for Shorts.

    Return ONLY valid JSON.

    JSON Format

    {{
    "long_videos":[
        {{
            "part":1,
            "title":"",
            "description":"",
            "hashtags":[],
            "tags":[],
            "thumbnail_text":"",
            "thumbnail_prompt":"",
            "chapters":[],
            "pinned_comment":""
        }}
    ],

    "shorts":[
        {{
            "index":1,
            "title":"",
            "description":"",
            "hashtags":[],
            "tags":[],
            "hook_text":"",
            "thumbnail_text":""
        }}
    ]
}}

    LONG VIDEOS

    {"".join(long_text)}

--------------------------------

SHORTS

    {"".join(short_text)}

    """

    ####################################################
    # OpenAI
    ####################################################

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
            .strip())
           
           print("=" * 80)
           print("RAW AI RESPONSE")
           print("=" * 80)
           print(response.output_text)
           print("=" * 80)

        data = json.loads(content)

        #    print("=" * 80)
        #    print("PARSED JSON")
        #    print("=" * 80)
        #    print(json.dumps(data, indent=4, ensure_ascii=False))

        

        return Metadata.model_validate(data)
    



    def correct_subtitles(
    self,
    subtitle: Subtitle) -> Subtitle:
        

        subtitle_json = json.dumps(
        subtitle.model_dump(),
        ensure_ascii=False,
        indent=2)

        prompt = f"""
        You are an expert editor for Indian Hindi and Hinglish call recordings .
        You are NOT a writer.
        You are NOT an editor.
        You are NOT allowed to improve sentences.

        Your ONLY job is to fix obvious speech-to-text mistakes.

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
