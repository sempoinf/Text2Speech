import torch
import torchaudio
from omegaconf import OmegaConf

import requests
# import numpy
import os

response = requests.get("https://github.com/snakers4/silero-models")
if response.status_code:
    print(response.status_code)  # Должно быть 200
    print(torchaudio.list_audio_backends())
else:
    exit("Error")

# torch.set_num_threads(4)
language = 'ru'
model_id = 'v4_ru'
device = torch.device('cpu')  # или 'cuda', если есть GPU
model, example_text = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                     model='silero_tts',
                                     language=language,
                                     speaker=model_id)
model.to(device)

# Пример текста
text = "Война и мир. Том 1. Часть 1. Глава 1."

print(text)

# Синтез речи
audio = model.apply_tts(text=text,
                        speaker='xenia',  # выбор голоса
                        sample_rate=48000,
                        put_accent=True,
                        put_yo=True)

# Преобразуем аудио в правильную форму [channels, samples]
audio = audio.unsqueeze(0)  # Добавляем канал, если audio имеет форму [samples]

# Проверка формы тензора
print(audio.shape)  # Должно быть [1, samples] 

# Сохранение в файл
torchaudio.save('output.wav', audio, sample_rate=48000, format='wav')
