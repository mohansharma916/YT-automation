from app.providers.openai.openai_provider import OpenAIProvider


class AIProviderFactory:

    @staticmethod
    def create():

        return OpenAIProvider()