# services/llm_providers/gemini_provider.py

import requests
from .base_provider import BaseLLMProvider

class GeminiProvider(BaseLLMProvider):
    """
    Провайдер для Google Gemini, использующий прямые REST API вызовы 
    через библиотеку requests для надежной работы с SOCKS-прокси.
    """
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/"

    def generate(self, model: str, system_prompt: str, user_prompt: str, temp: float):
        """
        Генерирует текст с помощью модели Gemini, отправляя запрос через прокси.
        """
        # 1. Формируем URL для запроса
        api_url = f"{self.base_url}{model}:generateContent?key={self.api_key}"

        # 2. Задаем настройки прокси из вашего примера
        # socks5h:// означает, что DNS-запросы также будут идти через прокси
        proxies = {
            'http': 'socks5://192.168.1.6:2080',
            'https': 'socks5h://192.168.1.6:2080'
        }

        # 3. Собираем тело запроса (payload) в формате, который ожидает Gemini API
        data = {
            "system_instruction": {
                "parts": {"text": system_prompt}
            },
            "contents": [{
                "parts": [{"text": user_prompt}]
            }],
            "generationConfig": {
                "temperature": temp
            }
        }
        
        try:
            # 4. Отправляем POST-запрос с данными и настройками прокси
            response = requests.post(api_url, json=data, proxies=proxies, timeout=90)
            
            # Проверяем, не вернул ли сервер ошибку (например, 4xx или 5xx)
            response.raise_for_status()

            # 5. Парсим JSON-ответ и извлекаем сгенерированный текст
            response_json = response.json()
            
            # Добавим проверку на случай, если контент был заблокирован
            if "candidates" not in response_json or not response_json["candidates"]:
                block_reason = response_json.get("promptFeedback", {}).get("blockReason", "неизвестная причина")
                error_message = f"Контент заблокирован. Причина: {block_reason}"
                return error_message, error_message

            text = response_json["candidates"][0]["content"]["parts"][0]["text"]
            return text, text

        except requests.exceptions.ProxyError as e:
            error_message = f"Ошибка подключения к прокси. Убедитесь, что Nekobox запущен и слушает порт 2080. Ошибка: {e}"
            print(error_message)
            return error_message, error_message
        except requests.exceptions.RequestException as e:
            # Ловим все остальные ошибки requests (таймаут, проблемы с сетью и т.д.)
            error_message = f"Произошла ошибка при обращении к API Gemini: {e}"
            print(error_message)
            return error_message, error_message
        except (KeyError, IndexError) as e:
            # Ловим ошибки, если структура JSON-ответа неожиданная
            error_message = f"Не удалось разобрать ответ от API Gemini. Структура ответа изменилась. Ошибка: {e}"
            print(error_message)
            return error_message, error_message