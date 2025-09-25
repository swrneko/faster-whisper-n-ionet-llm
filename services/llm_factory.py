# services/llm_factory.py
from services.llm_providers.ionet_provider import IoNetProvider
from services.llm_providers.gemini_provider import GeminiProvider
from services.llm_providers.gpt4free_provider import Gpt4FreeProvider
from services.llm_providers.base_provider import BaseLLMProvider

def get_llm_provider(provider_name: str, api_key: str | None) -> BaseLLMProvider:
    """
    Фабричная функция для получения экземпляра провайдера LLM.
    """
    if provider_name == 'io.net':
        if not api_key:
            raise ValueError("API ключ обязателен для io.net")
        return IoNetProvider(api_key)
    elif provider_name == 'Gemini':
        if not api_key:
            raise ValueError("API ключ обязателен для Gemini")
        return GeminiProvider(api_key)
    elif provider_name == 'gpt4free':
        return Gpt4FreeProvider()
    else:
        raise ValueError(f"Неизвестный провайдер: {provider_name}")