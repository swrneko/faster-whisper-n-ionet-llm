import gradio as gr
from faster_whisper import WhisperModel
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional
import os

from services.llm import Llm

load_dotenv()

# Стандартный API ключ
DEFAULT_API_KEY=os.getenv('API_KEY')
# Задаем выходную директорию
OUTPUT_PATH='outputs'
# Стандартный системный промпт
DEFAULT_SYSTEM_PROMPT='''You are a diligent university student who has recorded a lecture as an audio file and later transcribed it into raw text. 
Your task is to rewrite this unstructured transcript into a clear, logically organized, and detailed lecture summary (lecture notes).  

Guidelines:
1. Structure:
   - Organize the text into a hierarchy of sections and subsections.  
   - Use headings, bullet points, or numbering where appropriate.  
   - Present the material in a logical flow (from introduction → main points → details → examples → conclusion).  

2. Clarity & Cohesion:
   - Remove filler words, repetitions, and irrelevant fragments.  
   - Rewrite incomplete sentences into full, grammatically correct sentences.  
   - Ensure smooth transitions between topics, making the summary feel continuous and well-connected.  

3. Depth & Detail: 
   - Capture all important concepts, definitions, examples, and explanations from the lecture.  
   - Expand shorthand or fragmented thoughts into full, precise explanations.  
   - Where appropriate, rephrase or clarify confusing passages for better understanding.  

4. Accuracy:
   - Preserve the lecturer’s original meaning, intent, and terminology.  
   - Avoid adding personal opinions or new information that was not in the lecture.  

5. Style:
   - Write in a formal, academic tone suitable for study notes.  
   - Aim for readability: concise sentences, but thorough coverage of concepts.  
   - Use emphasis (e.g., bold or italic text) only when it improves comprehension.  

Final Output: A cohesive, detailed, and well-structured lecture summary, suitable for later studying and revision.
Use only russian language!
'''

faster_whisper_models_list = ['tiny', 'base', 'small', 'medium', 'large-v1', 'large-v2', 'large-v3', 'large', 'distil-large-v2', 'distil-large-v3', 'distil-large-v3.5', 'large-v3-turbo', 'turbo']
llm_models_list = ['openai/gpt-oss-120b', 'Qwen/Qwen3-235B-A22B-Thinking-2507', 'deepseek-ai/DeepSeek-R1-0528', 'meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8', 'openai/gpt-oss-20b', 'Intel/Qwen3-Coder-480B-A35B-Instruct-int4-mixed-ar', 'meta-llama/Llama-3.2-90B-Vision-Instruct', 'mistralai/Mistral-Nemo-Instruct-2407', 'Qwen/Qwen2.5-VL-32B-Instruct', 'meta-llama/Llama-3.3-70B-Instruct', 'mistralai/Devstral-Small-2505', 'mistralai/Magistral-Small-2506', 'mistralai/Mistral-Large-Instruct-2411', 'CohereForAI/aya-expanse-32b']

# Функция транскрибации
def recognize(model, audioFile, beamSize, vadFilter, minSilenceDurationMs, speechPadMs, temp0, temp1, temp2, wordTimestamps, noSpeechThreshold, conditionOnPreviousText):
    model = WhisperModel(model, device='cuda', compute_type='float16') # Задаем модель

    segments, _ = model.transcribe( # Распознаем текст
        audioFile,
        beam_size=beamSize,
        vad_filter=vadFilter,
        vad_parameters={
            "min_silence_duration_ms": minSilenceDurationMs,
            "speech_pad_ms": speechPadMs
        },
        temperature= [temp0, temp1, temp2],
        word_timestamps=wordTimestamps,
        no_speech_threshold=noSpeechThreshold,
        condition_on_previous_text=conditionOnPreviousText
    )

    text = ''

    for seg in segments:
        text += f"[{format_timestamp(seg.start)} -> {format_timestamp(seg.end)}] {seg.text}" + '\n'
    
    return(text)

def generateByCondition(api_key, llm_model, system_prompt, recognized_text, llm_temperature, is_pipeline_enabled, trigger, isSaveFile):
    llm = Llm(api_key)

    # если чекбокс включен и событие было change → обрабатываем
    if is_pipeline_enabled and trigger == "change":
        result, md = llm.generate(llm_model, system_prompt, recognized_text, llm_temperature)

        if isSaveFile:
            saveFile("output.txt", result)

        return result, result

    # если чекбокс выключен и событие было click → обрабатываем
    if not is_pipeline_enabled and trigger == "click":
        result, md = llm.generate(llm_model, system_prompt, recognized_text, llm_temperature)

        if isSaveFile:
            saveFile("output.txt", result)

        return result, md

    # если нет чекбокса и было событие change
    return gr.skip(), gr.skip()

def format_timestamp(seconds: float) -> str:
    millis = int(seconds * 1000)
    hours = millis // (3600 * 1000)
    minutes = (millis % (3600 * 1000)) // (60 * 1000)
    seconds_int = (millis % (60 * 1000)) // 1000
    millis = millis % 1000
    return f"{hours:02d}:{minutes:02d}:{seconds_int:02d},{millis:03d}"

# Функция сохранения файла
def saveFile(filename, text):
    directory = Path(OUTPUT_PATH)
    filePath = directory / filename
    filePath.parent.mkdir(parents=True, exist_ok=True)
    filePath.write_text(text, encoding='utf-8')

# Функция для динамического обновления кнопки в зависимости от состояния checkbox
def updateButton(isChecked):
    if not isChecked:
        variant = 'primary'
    else:
        variant = 'secondary'

    return gr.update(interactive=not isChecked, variant=variant)



def updateTextbox(isChecked):
    return gr.update(visible=isChecked)


# Интерфейс
with gr.Blocks() as demo:
    gr.HTML('''
    <div align=center>
        <h1>
            Faster Whisper WebUI
        </h1>
    </div>
    ''')

    with gr.Row():
        with gr.Column():
            # Колонка в левой части экрана с основным взаимодействием
            with gr.Accordion(label='Recognization'):
                with gr.Column():
                    audioFile = gr.Audio(label='Load audio for transcribe', type="filepath")
                    recognizeBtn = gr.Button('recognize', variant='primary')

                    with gr.Accordion(label='Recognized text'):
                        recognizedText = gr.TextArea(label='')

            # Колонка в правой части экрана с настройками
            with gr.Column():
                with gr.Accordion(label='Settings'):
                    # Первое поле на всю ширину в акордионе настроек
                    saveFileCheckbox = gr.Checkbox(label='save file', value=True, interactive=True)
                    filename = gr.Textbox(label='Output filename', value='output.txt', interactive=True)

                    # Акордион настроек faster whisper
                    with gr.Accordion(label='Faster whisper settings'):
                        with gr.Row():
                            # Левая колонка в акордионе
                            with gr.Column():
                                fastWhisperModel = gr.Dropdown(label='Model', choices=faster_whisper_models_list, interactive=True)

                                beamSize = gr.Number(label='beam_size', value=8, interactive=True)
                                noSpeechThreshold  = gr.Number(label='no_speech_threshold', value=0.5, interactive=True)
                                vadFilter = gr.Checkbox(label='vad_filter', value=True, interactive=True)
                                wordTimestamps = gr.Checkbox(label='word_timestamps', value=True, interactive=True)
                                conditionOnPreviousText = gr.Checkbox(label='condition_on_previous_text', value=False, interactive=True)

                            # Правая колонка в акордионе
                            with gr.Column():
                                with gr.Accordion(label='Vad parameters'):
                                    minSilenceDurationMs = gr.Number(label='min_silence_duration_ms', value=300, interactive=True)
                                    speechPadMs = gr.Number(label='speech_pad_ms', value=200, interactive=True)

                                with gr.Accordion(label='Temperature'):
                                    temp0 = gr.Number(label='temp_0', value=0.0, interactive=True)
                                    temp1 = gr.Number(label='temp_1', value=0.2, interactive=True)
                                    temp2 = gr.Number(label='temp_2', value=0.4, interactive=True)

                    # Нижний акордион настроек для api ключа llm
                    with gr.Accordion(label='ai.io.net api settings'):
                        apiKey = gr.Textbox(label='API key', value=DEFAULT_API_KEY, interactive=True)

                        with gr.Accordion(label='System prompt'):
                            systemPrompt = gr.Textbox(label='', value=DEFAULT_SYSTEM_PROMPT, interactive=True)

                        with gr.Row():
                            llmModel = gr.Dropdown(label='models', choices=llm_models_list, value=llm_models_list[0], interactive=True)
                            llmTemperature = gr.Number(label='Temperature', value=0.8, interactive=True )

        with gr.Column():
            with gr.Accordion(label='LLM'):
                isPipelineEnabledCheckbox = gr.Checkbox(label='is pipeline enabled', value=True, interactive=True)
                refineTextBtn = gr.Button('refine text', variant='secondary', interactive=False)

                with gr.Accordion(label='Refined text raw'):
                    refinedText = gr.Textbox(label='', show_copy_button=True)

                with gr.Accordion(label='Refined text md formated'):
                    refinedTextMD = gr.Markdown(label='')


    isPipelineEnabledCheckbox.change(updateButton, inputs=[isPipelineEnabledCheckbox], outputs=refineTextBtn)
    saveFileCheckbox.change(updateTextbox, inputs=saveFileCheckbox, outputs=filename)

    recognizeBtn.click(recognize, outputs=[recognizedText], inputs=[fastWhisperModel, audioFile, beamSize, vadFilter, minSilenceDurationMs, speechPadMs, temp0, temp1, temp2, wordTimestamps, noSpeechThreshold, conditionOnPreviousText])
    
    # Если пайплайн включен то тогда делаем автоматически
    # автоматический пайплайн
    recognizedText.change(
        generateByCondition,
        inputs=[apiKey, llmModel, systemPrompt, recognizedText, llmTemperature, isPipelineEnabledCheckbox, gr.State("change"), saveFileCheckbox],
        outputs=[refinedText, refinedTextMD]
    )

    # ручной запуск по кнопке
    refineTextBtn.click(
        generateByCondition,
        inputs=[apiKey, llmModel, systemPrompt, recognizedText, llmTemperature, isPipelineEnabledCheckbox, gr.State("click"), saveFileCheckbox],
        outputs=[refinedText, refinedTextMD]
    )


demo.launch()
