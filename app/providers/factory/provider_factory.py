

from app.providers.openai.openai_provider import (
    OpenAIProvider,
)
from app.providers.transcription.deeogram_provider import DeepgramProvider


class ProviderFactory:

    @staticmethod
    def transcription():

        return DeepgramProvider()

    @staticmethod
    def llm():

        return OpenAIProvider()