from pathlib import Path
from markdown_pdf import MarkdownPdf # Для аннотации типов

class FileHandlers:
    # Функция сохранения файла
    def saveFile(self, filename, content, output_path):
        '''
        Сохраняет текст или pdf из markdown_pdf в файл с указанным названием и директорией.

        Args:
            :param filename: название файла;
            :param content: содержание файла;
            :param output_path: выходная диретория файла.
        '''
        # Создание объекта директории
        directory = Path(output_path)
        filePath = directory / filename # Добавление пути директории
        filePath.parent.mkdir(parents=True, exist_ok=True) # Создание директории если не существует
        # Сохранение для разных типов
        if type(content) == MarkdownPdf:
            content.save(filePath)
        elif type(content) == str:
            filePath.write_text(content, encoding='utf-8')
