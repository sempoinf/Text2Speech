from lib_speak import Speaker
from lib_sl_text import SeleroText
import os

text = SeleroText("Пример текста для синтеза речи")
speaker = Speaker(model_id="ru_v3", language="ru", speaker="aidar", device="cpu")
speaker.to_mp3(text=text, name_text="Текст", sample_rate=48000, audio_dir=pathlib.Path(__file__).parent.parent / "mp3", speed=1.0)