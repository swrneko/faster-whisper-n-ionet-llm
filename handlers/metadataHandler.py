import os
from PIL import Image, ExifTags
import subprocess
import json
from datetime import datetime

class MetadataHandler:
    def get_image_timestamp(self, image_path: str) -> datetime | None: 
        """Извлекает метку времени из метаданных изображения, если она доступна."""
        try:
            image = Image.open(image_path)
            exif_data = image._getexif()
            if exif_data:
                for tag, value in exif_data.items():
                    decoded_tag = ExifTags.TAGS.get(tag, tag)
                    if decoded_tag == 'DateTimeOriginal':
                        return value
            return None
        except Exception as e:
            print(f"Error extracting metadata from image: {e}")
            return None