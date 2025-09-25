# services/llm_providers/gpt4free_provider.py
from g4f.client import Client
from .base_provider import BaseLLMProvider

class Gpt4FreeProvider(BaseLLMProvider):
    # gpt4free не требует API ключа
    def __init__(self, api_key: str | None = None):
        super().__init__(api_key)
        self.client = Client()


    def generate(self, model: str, system_prompt: str, user_prompt: str, temp: float):
        # temp в g4f может работать не для всех внутренних провайдеров
        try:
            response = self.client.chat.completions.create(
            model=model,  # Пример модели, может варьироваться в зависимости от доступности провайдеров
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
                ],
                temperature=temp
            )
            text = response.choices[0].message.content
            return text, text
        except Exception as e:
            error_message = f"Ошибка при работе с gpt4free: {e}"
            print(error_message)
            return error_message, error_message