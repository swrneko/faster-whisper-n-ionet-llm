class GradioHandlers:
    def __init__(self, gr, Llm, ConvertMdToPdf, FileHandlers, FasterWhisper):
        # Объект для работы с файлами
        self.fh = FileHandlers()
        self.ConvertMdToPdf = ConvertMdToPdf()
        self.FasterWhisper = FasterWhisper()
        self.Llm = Llm
        self.gr = gr

    # Функция улучшения текста
    def generateByCondition(self, api_key, llm_model, system_prompt, recognized_text, llm_temperature, is_pipeline_enabled, trigger, isSaveFile, filename, filenamePdf, output_path):
        llm = self.Llm(api_key)

        # если чекбокс включен и событие было change → обрабатываем
        if is_pipeline_enabled and trigger == "change":
            result, md = llm.generate(llm_model, system_prompt, recognized_text, llm_temperature)

            # Конвертируем текст с латексом в юникод
            pdf, unicodeText = self.ConvertMdToPdf.convertLatexToText(md)

            if isSaveFile:
                self.fh.saveFile(filenamePdf, pdf, output_path)
                self.fh.saveFile(filename, result, output_path)

            return result, unicodeText

        # если чекбокс выключен и событие было click → обрабатываем
        if not is_pipeline_enabled and trigger == "click":
            result, md = llm.generate(llm_model, system_prompt, recognized_text, llm_temperature)

            # Конвертируем текст с латексом в юникод
            pdf, unicodeText = self.ConvertMdToPdf.convertLatexToText(md)

            if isSaveFile:
                self.fh.saveFile(filenamePdf, pdf, output_path)
                self.fh.saveFile(filename, result, output_path)

            return result, unicodeText

        # если нет чекбокса и было событие change
        return self.gr.skip(), self.gr.skip()

    # Функция для динамического обновления кнопки в зависимости от состояния checkbox
    def updateButton(self, isChecked):
        if not isChecked:
            variant = 'primary'
        else:
            variant = 'secondary'

        return self.gr.update(interactive=not isChecked, variant=variant)


    def updateTextbox(self, isChecked):
        return self.gr.update(visible=isChecked)

