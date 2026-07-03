from app.providers.transcription.sarvam_provider import SarvamProvider


class TranscriptionProviderFactory:

    @staticmethod
    def create():

        return SarvamProvider()