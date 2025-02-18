import torch
import os
import re
import sys
import requests

class TextChunker:
    def __init__(self, max_length=181):
        self.max_length = max_length

    def split_text(self, text):
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks = []
        current_chunk = ""

        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= self.max_length:
                current_chunk += " " + sentence if current_chunk else sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def from_file(self, file_path, split=False):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        if split == True:
            return self.split_text(text)
        else:
            return text  
    
    def from_url(self, url, split=False):
        response = requests.get(url)
        if response.status_code == 200:
            text = response.text
            if split == True:
                return self.split_text(text)
            else:
                return text
        else:
            raise Exception(f"Ошибка загрузки текста: {response.status_code}")
    
TTS_REPO_PATH = os.path.abspath("/Users/yaao20u291/Documents/Pets/inc/TTS")  # Папка, куда ты клонировал TTS
sys.path.insert(0, TTS_REPO_PATH)
from TTS.api import TTS

class CoquiTTS:
    def __init__(self, model_name: str = "tts_models/multilingual/multi-dataset/xtts_v2", gpu: bool = False):
        """
        Инициализация TTS модели.
        :param model_name: Имя модели, загружаемой из Coqui TTS.
        :param gpu: Использовать ли GPU.
        """
        self.device = "cuda" if gpu and torch.cuda.is_available() else "cpu"
        self.model = TTS(model_name).to(self.device)

    def synthesize(self, text: str, output_path: str, speaker: str = None, language: str = None):
        """
        Синтезирует речь из текста и сохраняет в файл.
        :param text: Входной текст.
        :param output_path: Путь для сохранения аудиофайла.
        :param speaker: Опциональный параметр выбора диктора.
        :param language: Опциональный параметр выбора языка.
        """
        self.model.tts_to_file(
            text=text,
            file_path=output_path,
            speaker=speaker,
            language=language
        )
        print(f"Аудиофайл сохранен: {output_path}")
    
    def available_speakers(self):
        """Возвращает список доступных дикторов."""
        return self.model.speakers if hasattr(self.model, 'speakers') else None
    
    def available_languages(self):
        """Возвращает список доступных языков."""
        return self.model.languages if hasattr(self.model, 'languages') else None

if __name__ == "__main__":
    chunker = TextChunker()
    # text = "Небо было пасмурным, а тёмные облака подавляли величественную атмосферу Дворца. Великолепный дворцовый зал был окутан тёмными облаками, как будто это была огромная клетка, крепко удерживающая людей."
    # print(len(text))
    # formated_txt = chunker.split_text(text)
    # print(len(formated_txt)) # out 2, cause 198 symbs
    test_txt = chunker.from_file(r'/Users/yaao20u291/Documents/Pets/test_text.txt', split=True)
    # print(test_txt)
    print(len(test_txt))
    # exit()
    
    tts = CoquiTTS(gpu=True)
    # model_name = "tts_models/multilingual/multi-dataset/xtts_v2"

    for segment in test_txt:
        path_save_file = r"output/coqui/test.wav"
        tts.synthesize(test_txt, path_save_file, speaker= 'Baldur Sanjin', language="ru")