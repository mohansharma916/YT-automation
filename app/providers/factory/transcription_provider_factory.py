from app.providers.transcription.deeogram_provider import DeepgramProvider
from app.providers.transcription.sarvam_provider import SarvamProvider


class TranscriptionProviderFactory:

    @staticmethod
    def transcription():

        return DeepgramProvider()