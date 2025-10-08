from pydub import AudioSegment

class GlueAudio():
    def glue(self, audio_files: list, output_path: str, output_filename: str) -> Path:
        """
        Склеивает аудиофайлы с помощью FFmpeg, используя промежуточный список файлов.
        Этот метод чрезвычайно эффективен по памяти и скорости.

        Args:
            audio_files (list): Список путей к исходным аудиофайлам.
            output_path (str): Директория для сохранения итогового файла.
            output_filename (str): Имя итогового склеенного файла.

        Returns:
            Path: Путь к созданному склеенному файлу.
        """

