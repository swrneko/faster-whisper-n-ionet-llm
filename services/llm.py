import openai

class Llm:
    def __init__(self, apiKey:str):
        self.client = openai.OpenAI(
            api_key=apiKey,
            base_url='https://api.intelligence.io.solutions/api/v1/'
        )

    def generate(self, model:str, systemPrompt:str, userPrompt:str, temp:float):
        '''
        prompt[user_promtp, system_ptompt]
        Function generate text by prompt
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

