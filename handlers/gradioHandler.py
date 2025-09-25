from config import LLM_MODELS # Импортируем словарь моделей
import gradio as gr 


class GradioHandlers:
    def __init__(self, llm_factory, ConvertMdToPdf, FileHandlers, FasterWhisper, GlueAudio):
        # Объект для работы с файлами
        self.fh = FileHandlers()
        self.ga = GlueAudio()
        self.ConvertMdToPdf = ConvertMdToPdf()
        self.FasterWhisper = FasterWhisper()
        self.llm_factory = llm_factory # Сохраняем фабрику

    def handleRecognizeBtn(self, audioFiles, model, device, compute_type, beamSize, vadFilter, minSilenceDurationMs, speechPadMs, temp0, temp1, temp2, wordTimestamps, noSpeechThreshold, conditionOnPreviousText, filename, outPath):
        audioFile = self.ga.glue(audioFiles)
        file = self.fh.saveFile(filename, audioFile, outPath)

        return self.FasterWhisper.recognize(model, device, compute_type, file, beamSize, vadFilter, minSilenceDurationMs, speechPadMs, temp0, temp1, temp2, wordTimestamps, noSpeechThreshold, conditionOnPreviousText)

    # Функция улучшения текста
    def generateByCondition(self, api_key, llm_provider, llm_model, system_prompt, recognized_text, llm_temperature, is_pipeline_enabled, trigger, isSaveFile, filename, filenamePdf, output_path):
        try:
            # Получаем нужный провайдер через фабрику
            provider = self.llm_factory(llm_provider, api_key)
        except ValueError as e:
            # Если API ключ не предоставлен для нужного провайдера, выводим ошибку
            self.gr.Warning(str(e))
            return self.gr.skip(), self.gr.skip()

        def process():
            result, md = provider.generate(llm_model, system_prompt, recognized_text, llm_temperature)
            pdf, unicodeText = self.ConvertMdToPdf.convertLatexToText(md)
            if isSaveFile:
                self.fh.saveFile(filenamePdf, pdf, output_path)
                self.fh.saveFile(filename, result, output_path)
            return result, unicodeText

        if (is_pipeline_enabled and trigger == "change") or (not is_pipeline_enabled and trigger == "click"):
            return process()

        return gr.skip(), gr.skip()
    
    # НОВАЯ ФУНКЦИЯ для обновления списка моделей
    def update_model_dropdown(self, provider):
        """
        Вызывается при изменении llmProvider.
        Возвращает обновленный компонент Dropdown для моделей.
        """
        # Получаем список моделей для выбранного провайдера
        models = LLM_MODELS.get(provider, [])
        
        # Выбираем первое значение по умолчанию, если список не пуст
        default_value = models[0] if models else None
        
        # Возвращаем обновленный компонент. Используем 'gr' напрямую.
        return gr.update(choices=models, value=default_value)

     # Функция для динамического обновления кнопки
    def updateButton(self, isChecked):
        if not isChecked:
            variant = 'primary'
        else:
            variant = 'secondary'
        return gr.update(interactive=not isChecked, variant=variant)

    def updateTextbox(self, isChecked):
        return gr.update(visible=isChecked)