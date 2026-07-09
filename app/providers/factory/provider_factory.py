from app.providers.openai.openai_provider import OpenAIProvider
from app.providers.transcription.openai_provider import (
    OpenAITranscriptionProvider,
)


class ProviderFactory:

    @staticmethod
    def transcription():

        return OpenAITranscriptionProvider()

    @staticmethod
    def llm():

        return OpenAIProvider()