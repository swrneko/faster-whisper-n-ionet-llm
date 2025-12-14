from config import LLM_MODELS, GEMINI_API_KEY, IO_API_KEY
import gradio as gr 

class GradioHandlers:
    def __init__(self, llm_factory, ConvertMdToPdf, FileHandlers, FasterWhisper, GlueAudio):
        self.fh = FileHandlers()
        self.ga = GlueAudio()
        self.ConvertMdToPdf = ConvertMdToPdf()
        self.FasterWhisper = FasterWhisper()
        self.llm_factory = llm_factory 

    def handleRecognizeBtn(self, audioFiles, model, device, compute_type, beamSize, vadFilter, 
            minSilenceDurationMs, speechPadMs, temp0, temp1, temp2, 
            wordTimestamps, noSpeechThreshold, conditionOnPreviousText, filename, outPath):
        try:
            glued_audio_path = self.ga.glue(
                audio_files=[f.name for f in audioFiles], 
                output_path=outPath,
                output_filename=filename
            )
        except (FileNotFoundError, RuntimeError) as e:
            gr.Warning(str(e))
            return "" 

        return self.FasterWhisper.recognize(model, device, compute_type, str(glued_audio_path), beamSize, vadFilter, minSilenceDurationMs, speechPadMs, temp0, temp1, temp2, wordTimestamps, noSpeechThreshold, conditionOnPreviousText)

    # Добавил аргумент custom_base_url в конец
    def generateByCondition(self, api_key, llm_provider, 
                            llm_model, system_prompt, recognized_text, 
                            llm_temperature, is_pipeline_enabled, trigger, 
                            isSaveFile, filename, filenamePdf, output_path, custom_base_url):
        
        try:
            if llm_provider == "Custom":
                # Передаем base_url только для Custom
                provider = self.llm_factory(llm_provider, api_key, base_url=custom_base_url)
            else:
                provider = self.llm_factory(llm_provider, api_key)
        except ValueError as e:
            gr.Warning(str(e))
            return gr.skip(), gr.skip()

        def process():
            # Добавлена обработка ошибок генерации
            try:
                result, md = provider.generate(llm_model, system_prompt, recognized_text, llm_temperature)
            except Exception as e:
                raise gr.Error(f"Ошибка генерации LLM: {e}")

            pdf, unicodeText = self.ConvertMdToPdf.convertLatexToText(md)
            if isSaveFile:
                self.fh.saveFile(filenamePdf, pdf, output_path)
                self.fh.saveFile(filename, result, output_path)
            return result, unicodeText

        if (is_pipeline_enabled and trigger == "change") or (not is_pipeline_enabled and trigger == "click"):
            return process()

        return gr.skip(), gr.skip()
    
    def update_model_dropdown(self, provider):
        models = LLM_MODELS.get(provider, [])
        default_value = models[0] if models else None
        
        # Обновляем список моделей и настройки поля API Key
        if provider == 'io.net': 
            return gr.update(choices=models, value=default_value), gr.update(label='API key', value=IO_API_KEY, interactive=True, visible=True)
        if provider == 'Gemini': 
            return gr.update(choices=models, value=default_value), gr.update(label='API key', value=GEMINI_API_KEY, interactive=True, visible=True)
        if provider == 'gpt4free': 
            return gr.update(choices=models, value=default_value), gr.update(label='API key (not required)', value="", interactive=False, visible=True)
        if provider == "Custom": 
            return gr.update(choices=models, value=default_value), gr.update(label='API key (optional)', value="", interactive=True, visible=True) # Для Custom ключ может понадобиться

    def updateButton(self, isChecked):
        variant = 'secondary' if isChecked else 'primary'
        return gr.update(interactive=not isChecked, variant=variant)
    
    def toggle_custom_url(self, provider):
        """Показывает поле Base URL только если выбран Custom"""
        return gr.update(visible=(provider == 'Custom'))
    
    def update_custom_url(self, base_url):
        return None 

    def updateTextbox(self, isChecked):
        return gr.update(visible=isChecked)