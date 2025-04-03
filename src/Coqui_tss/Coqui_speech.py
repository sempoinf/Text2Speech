import torch
from itertools import islice

# TTS_REPO_PATH = os.path.abspath("../Pets/Text2Speech/inc/TTS") 
# sys.path.insert(0, TTS_REPO_PATH)
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
        print(f"Audio is saved: {output_path}")
    
    def available_speakers(self):
        """Возвращает список доступных дикторов."""
        return self.model.speakers if hasattr(self.model, 'speakers') else None
    
    def available_languages(self):
        """Возвращает список доступных языков."""
        return self.model.languages if hasattr(self.model, 'languages') else None
    

if __name__ == "__main__":
    model_name = r"tts_models/multilingual/multi-dataset/xtts_v2"
    tts = CoquiTTS(model_name=model_name ,gpu=True)
    test_txt = "Небо было пасмурным, а тёмные облака подавляли величественную атмосферу Дворца. Великолепный дворцовый зал был окутан тёмными облаками, как будто это была огромная клетка, крепко удерживающая людей."
    path_save_file = r"data/output/test.mp3"
    tts.synthesize(test_txt, path_save_file, speaker= 'Baldur Sanjin', language="ru")
    print(f"Complete")
   
    # print(tts.available_languages())
    # print(tts.available_speakers())