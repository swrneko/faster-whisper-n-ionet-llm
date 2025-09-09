import gradio as gr
from pathlib import Path

# Подгрузка сервисов
from services.llm import Llm
from services.fasterWhisper import FasterWhisper
from services.convertMdToPdf import ConvertMdToPdf

# Загрузка параметров конфигурации
from config import *

# Функция транскрибации
def generateByCondition(api_key, llm_model, system_prompt, recognized_text, llm_temperature, is_pipeline_enabled, trigger, isSaveFile, filename, filenamePdf):
    llm = Llm(api_key)

    # если чекбокс включен и событие было change → обрабатываем
    if is_pipeline_enabled and trigger == "change":
        result, md = llm.generate(llm_model, system_prompt, recognized_text, llm_temperature)

        # Конвертируем текст с латексом в юникод
        pdf, unicodeText = ConvertMdToPdf().convertLatexToText(md)

        if isSaveFile:
            savePdf(filenamePdf, pdf)
            saveFile(filename, result)

        return result, unicodeText

    # если чекбокс выключен и событие было click → обрабатываем
    if not is_pipeline_enabled and trigger == "click":
        result, md = llm.generate(llm_model, system_prompt, recognized_text, llm_temperature)

        # Конвертируем текст с латексом в юникод
        pdf, unicodeText = ConvertMdToPdf().convertLatexToText(md)

        if isSaveFile:
            savePdf(filenamePdf, pdf)
            saveFile(filename, result)

        return result, unicodeText

    # если нет чекбокса и было событие change
    return gr.skip(), gr.skip()


def savePdf(filename, pdf):
    directory = Path(OUTPUT_PATH)
    filePath = directory / filename
    filePath.parent.mkdir(parents=True, exist_ok=True)
    pdf.save(filePath)

# Функция сохранеhния файла
def saveFile(filename, text):
    directory = Path(OUTPUT_PATH)
    filePath = directory / filename
    filePath.parent.mkdir(parents=True, exist_ok=True)
    filePath.write_text(text, encoding='utf-8')

#    ConvertMdToPdf().convert(text)

# Функция для динамического обновления кнопки в зависимости от состояния checkbox
def updateButton(isChecked):
    if not isChecked:
        variant = 'primary'
    else:
        variant = 'secondary'

    return gr.update(interactive=not isChecked, variant=variant)


def updateTextbox(isChecked):
    return gr.update(visible=isChecked)

###################################################
# ____ ___.___  ___.          .__                 #
#|    |   \   | \_ |__   ____ |  |   ______  _  __#
#|    |   /   |  | __ \_/ __ \|  |  /  _ \ \/ \/ /#
#|    |  /|   |  | \_\ \  ___/|  |_(  <_> )     / #
#|______/ |___|  |___  /\___  >____/\____/ \/\_/  #
#                    \/     \/                    #
###################################################

with gr.Blocks() as demo:
    gr.HTML('''
    <div align=center>
        <h1>
            Faster Whisper WebUI
        </h1>
    </div>
    ''')

    with gr.Row():
        # Вкладка с основным взаимодействием
        with gr.Tab('Actions'):
            isPipelineEnabledCheckbox = gr.Checkbox(label='is pipeline enabled', value=True, interactive=True)

            with gr.Row():
                with gr.Accordion(label='Recognization and integration'):
                    with gr.Column():
                        audioFile = gr.Audio(label='Load audio for transcribe', type="filepath")
                        images = gr.Files(label='Upload images', file_types=['image'])
                        recognizeBtn = gr.Button('recognize and integrate', variant='primary')

                        with gr.Accordion(label='Recognized text'):
                            recognizedText = gr.TextArea(label='')

                with gr.Accordion(label='LLM'):
                    with gr.Column():
                        refineTextBtn = gr.Button('refine text', variant='secondary', interactive=False)

                        with gr.Accordion(label='Refined text raw'):
                            refinedText = gr.Textbox(label='', show_copy_button=True)

                        with gr.Accordion(label='Refined text md formated'):
                            refinedTextMD = gr.Markdown(label='')

        # Вкладка с настройками
        with gr.Tab('Settings'):
            with gr.Column():
                # Первое поле на всю ширину в акордионе настроек
                with gr.Accordion('File settings'):
                    saveFileCheckbox = gr.Checkbox(label='save file', value=True, interactive=True)
                    filename = gr.Textbox(label='Output filename', value='output.txt', interactive=True)
                    filenamePdf = gr.Textbox(label='Output filename for pdf', value='output.pdf', interactive=True)

                # Акордион настроек faster whisper
                with gr.Accordion(label='Faster whisper settings'):
                    with gr.Row():
                        # Левая колонка в акордионе
                        with gr.Column():
                            fastWhisperModel = gr.Dropdown(label='Model', choices=FAST_WHISPER_MODELS, value=FAST_WHISPER_MODELS[11], interactive=True)

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
                        llmModel = gr.Dropdown(label='models', choices=LLM_MODELS, value=LLM_MODELS[1], interactive=True)
                        llmTemperature = gr.Number(label='Temperature', value=0.8, interactive=True )

    ######################################################################
    #.____                 .__         ___.          .__                 #
    #|    |    ____   ____ |__| ____   \_ |__   ____ |  |   ______  _  __#
    #|    |   /  _ \ / ___\|  |/ ___\   | __ \_/ __ \|  |  /  _ \ \/ \/ /#
    #|    |__(  <_> ) /_/  >  \  \___   | \_\ \  ___/|  |_(  <_> )     / #
    #|_______ \____/\___  /|__|\___  >  |___  /\___  >____/\____/ \/\_/  #
    #        \/    /_____/         \/       \/     \/                    #
    ######################################################################

    isPipelineEnabledCheckbox.change(updateButton, inputs=[isPipelineEnabledCheckbox], outputs=refineTextBtn)
    saveFileCheckbox.change(updateTextbox, inputs=saveFileCheckbox, outputs=filename)
    saveFileCheckbox.change(updateTextbox, inputs=saveFileCheckbox, outputs=filenamePdf)

    recognizeBtn.click(FasterWhisper().recognize, outputs=[recognizedText], inputs=[fastWhisperModel, audioFile, beamSize, vadFilter, minSilenceDurationMs, speechPadMs, temp0, temp1, temp2, wordTimestamps, noSpeechThreshold, conditionOnPreviousText])
    
    # Если пайплайн включен то тогда делаем автоматически
    # автоматический пайплайн
    recognizedText.change(
        generateByCondition,
        inputs=[apiKey, llmModel, systemPrompt, recognizedText, llmTemperature, isPipelineEnabledCheckbox, gr.State("change"), saveFileCheckbox, filename, filenamePdf],
        outputs=[refinedText, refinedTextMD]
    )

    # ручной запуск по кнопке
    refineTextBtn.click(
        generateByCondition,
        inputs=[apiKey, llmModel, systemPrompt, recognizedText, llmTemperature, isPipelineEnabledCheckbox, gr.State("click"), saveFileCheckbox, filename, filenamePdf],
        outputs=[refinedText, refinedTextMD]
    )

demo.launch()
