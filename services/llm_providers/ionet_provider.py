import requests
from .base_provider import BaseLLMProvider

class IoNetProvider(BaseLLMProvider):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.base_url = 'https://api.intelligence.io.solutions/api/v1'

    def generate(self, model: str, system_prompt: str, user_prompt: str, temp: float):
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": model,
            "messages": [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt},
            ],
            "temperature": temp
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            text = str(result['choices'][0]['message']['content'])
            return text, text  # Возвращаем как чистый текст, так и Markdown
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при запросе к IO.net API: {e}")