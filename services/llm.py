import openai

class Llm:
    def __init__(self, apiKey:str):
        self.client = openai.OpenAI(
            api_key=apiKey,
            base_url='https://api.intelligence.io.solutions/api/v1/'
        )

    def generate(self, model:str, systemPrompt:str, userPrompt:str, temp:float):
        '''
        Функция для генирации текста по промпту.

        Args:
            :param model: модель llm;
            :param systemPrompt: системный промпт;
            :param userPrompt: основной промпт промпт;
            :param temp: температура генерации.
        '''

        # Получаем ответ от нейросети
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {'role': 'system', 'content': systemPrompt},
                {'role': 'user', 'content': userPrompt},
            ],
            temperature=temp,
            stream=False
        ) 

        # Достаем текст
        text = str(response.choices[0].message.content)

        return text, text

