import openai
from .base_provider import BaseLLMProvider

class IoNetProvider(BaseLLMProvider):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.client = openai.OpenAI(
            api_key=self.api_key,
            base_url='https://api.intelligence.io.solutions/api/v1/'
        )

    def generate(self, model: str, system_prompt: str, user_prompt: str, temp: float):
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt},
            ],
            temperature=temp,
            stream=False
        )
        text = str(response.choices[0].message.content)
        return text, text # Возвращаем как чистый текст, так и Markdown