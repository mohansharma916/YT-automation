from app.providers.openai.openai_provider import OpenAIProvider


class ProviderFactory:

    @staticmethod
    def create():

        return OpenAIProvider()