from pathlib import Path

# Для аннотации типов
from markdown_pdf import MarkdownPdf 
from pydub import AudioSegment

class FileHandlers:
    # Функция сохранения файла
    def saveFile(self, filename, content, output_path, format='mp3'):
        '''
        Сохраняет текст, pdf из markdown_pdf или склеенный аудиофайл в файл с указанным названием и директорией.

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
            return content.save(filePath)

        elif type(content) == str:
            return filePath.write_text(content, encoding='utf-8')

        elif type(content) == AudioSegment:
            return content.export(filePath, format=format)
