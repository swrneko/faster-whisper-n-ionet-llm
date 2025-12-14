# services/llm_factory.py
from services.llm_providers.ionet_provider import IoNetProvider
from services.llm_providers.gemini_provider import GeminiProvider
from services.llm_providers.gpt4free_provider import Gpt4FreeProvider
from services.llm_providers.base_provider import BaseLLMProvider
from services.llm_providers.custom_provider import CustomProvider

def get_llm_provider(provider_name: str, api_key: str | None = None, base_url: str | None = None) -> BaseLLMProvider:
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
    elif provider_name == 'Custom':
        if not base_url:
            raise ValueError("Base URL обязателен для Custom провайдера")
        return CustomProvider(api_key, base_url)  # base_url будет установлен позже
    else:
        raise ValueError(f"Неизвестный провайдер: {provider_name}")