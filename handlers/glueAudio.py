import subprocess
from pathlib import Path


class GlueAudio():
    def glue(self, audio_files: list, output_path: str, output_filename: str) -> Path:
        """
        Склеивает аудиофайлы РАЗНЫХ форматов с помощью FFmpeg и filter_complex.
        Это универсальный и эффективный по памяти метод.

        Args:
            audio_files (list): Список путей к исходным аудиофайлам.
            output_path (str): Директория для сохранения итогового файла.
            output_filename (str): Имя итогового склеенного файла.

        Returns:
            Path: Путь к созданному склеенному файлу.
        """
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)
        final_audio_path = output_dir / output_filename

        if not audio_files:
            raise ValueError("Список аудиофайлов для склейки пуст.")

        # 1. Формируем часть команды с входными файлами (-i file1 -i file2 ...)
        input_args = []
        for file_path in audio_files:
            input_args.extend(['-i', str(Path(file_path).resolve())])

        # 2. Формируем строку для filter_complex
        num_files = len(audio_files)
        stream_specifiers = "".join([f"[{i}:a]" for i in range(num_files)])
        filter_complex_str = f"{stream_specifiers}concat=n={num_files}:v=0:a=1[outa]"

        # 3. Собираем полную команду
        command = [
            'ffmpeg',
            *input_args,  # Распаковываем список входных файлов
            '-filter_complex', filter_complex_str,
            '-map', '[outa]',
            '-c:a', 'libmp3lame',
            '-q:a', '2',
            str(final_audio_path),
            '-y'
        ]

        try:
            # 4. Выполняем команду
            print(f"Выполнение команды FFmpeg: {' '.join(command)}")
            subprocess.run(command, check=True, capture_output=True, text=True)
            print("FFmpeg успешно завершил склейку.")

        except FileNotFoundError:
            raise FileNotFoundError("FFmpeg не найден. Убедитесь, что он установлен и доступен в системной переменной PATH.")
        except subprocess.CalledProcessError as e:
            print("Ошибка при выполнении FFmpeg!")
            print("Stderr:", e.stderr)
            raise RuntimeError(f"Ошибка FFmpeg при склейке файлов: {e.stderr}")
        
        return final_audio_path