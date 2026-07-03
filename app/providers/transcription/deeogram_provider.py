from pathlib import Path

from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)

from app.config.settings import settings
from app.models.subtitle import Subtitle
from app.models.subtitle import SubtitleSegment
from app.providers.base.transcription_provider import (
    TranscriptionProvider,
)


class DeepgramProvider(TranscriptionProvider):

    def __init__(self):

        self.client = DeepgramClient(
            settings.deepgram_api_key,
        )

    def transcribe(
        self,
        audio_path: Path,
    ) -> Subtitle:

        with open(audio_path, "rb") as f:

            payload: FileSource = {
                "buffer": f.read(),
            }

        options = PrerecordedOptions(

            model="nova-3",

            smart_format=True,

            punctuate=True,

            paragraphs=True,

            utterances=True,

            diarize=False,

            detect_language=True,

        )

        response = (
            self.client.listen.rest.v("1").transcribe_file(
                payload,
                options,
            )
        )

        words = (
            response.results.channels[0]
            .alternatives[0]
            .words
        )

        segments = []

        current_words = []
        start = None

        for word in words:

            if start is None:
                start = word.start

            current_words.append(word.word)

            if (
                word.word.endswith(".")
                or word.word.endswith("?")
                or word.word.endswith("!")
                or len(current_words) >= 8
            ):

                segments.append(

                    SubtitleSegment(

                        start=start,

                        end=word.end,

                        text=" ".join(current_words),

                    )

                )

                current_words = []
                start = None

        if current_words:

            segments.append(

                SubtitleSegment(

                    start=start,

                    end=words[-1].end,

                    text=" ".join(current_words),

                )

            )

        return Subtitle(
            segments=segments,
        )