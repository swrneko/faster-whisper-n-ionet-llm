from abc import ABC, abstractmethod

class BaseLLMProvider(ABC):
    """
    Абстрактный базовый класс для всех провайдеров LLM.
    Каждый провайдер должен реализовать метод generate.
    """
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key

    @abstractmethod
    def generate(self, model: str, system_prompt: str, user_prompt: str, temp: float):
        """
        Основной метод для генерации текста.

        Должен возвращать кортеж из двух строк: (чистый_текст, markdown_текст)
        """
        pass