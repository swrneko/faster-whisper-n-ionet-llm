# services/llm_providers/gpt4free_provider.py
from g4f.client import Client
from .base_provider import BaseLLMProvider

class Gpt4FreeProvider(BaseLLMProvider):
    """
    Провайдер для работы с моделью GPT через библиотеку gpt4free.
    
    Этот класс реализует интерфейс BaseLLMProvider и предоставляет возможность
    взаимодействия с различными LLM через сервис gpt4free, который не требует
    API ключа для работы.
    """
    # gpt4free не требует API ключа
    def __init__(self, api_key: str | None = None):
        super().__init__(api_key)
        self.client = Client()


    def generate(self, model: str, system_prompt: str, user_prompt: str, temp: float):
        """
        Генерирует ответ от модели GPT с использованием gpt4free.
        
        Args:
            model (str): Название модели для генерации ответа
            system_prompt (str): Системное сообщение для контекста
            user_prompt (str): Пользовательский запрос
            temp (float): Температура генерации ( controls randomness of responses)
            
        Returns:
            tuple: Кортеж из двух одинаковых строк - сгенерированного ответа и его копии
        """
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