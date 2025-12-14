import requests
from .base_provider import BaseLLMProvider

class CustomProvider(BaseLLMProvider):
    def __init__(self, api_key: str | None = None, base_url: str | None = None):
        super().__init__(api_key)
        self.base_url = base_url or 'http://127.0.0.1:1234/v1/'
        
        # ГАРАНТИРУЕМ наличие слеша в конце URL
        if not self.base_url.endswith('/'):
            self.base_url += '/'

    def generate(self, model: str, system_prompt: str, user_prompt: str, temp: float):
        url = f"{self.base_url}chat/completions"
        
        # Некоторые Custom провайдеры (как vLLM или Ollama) могут требовать API Key, даже если он фиктивный
        headers = {"Content-Type": "application/json"}
        if self.api_key:
             headers["Authorization"] = f"Bearer {self.api_key}"

        data = {
            "model": model,
            "messages": [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt},
            ],
            "temperature": temp,
            "stream": False
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=300)
            response.raise_for_status()
            result = response.json()
            
            # Обработка разных форматов ответа (на всякий случай)
            if 'choices' in result and len(result['choices']) > 0:
                text = str(result['choices'][0]['message']['content'])
                return text, text
            else:
                return f"Неожиданный ответ от сервера: {result}", str(result)
            
        except requests.exceptions.RequestException as e:
            return f"Ошибка при запросе к CustomProvider API: {e}", f"Ошибка: {e}"