from transformers import AutoProcessor, BarkModel
import scipy
import torch
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../inc/VALL_EX')))

# Загрузка процессора и модели
processor = AutoProcessor.from_pretrained("suno/bark")
model = BarkModel.from_pretrained("suno/bark")
# model = BarkModel.from_pretrained("suno/bark-small", torch_dtype=torch.float16, attn_implementation="flash_attention_2").to(device)

# Настройка русского голоса
voice_preset = "v2/ru_speaker_4"

text_sample = "Заоблачный утёс Божественной Тайной горы был самым пугающим из четырех смертоносных мест Континента Лазурного Облака." \
                "Этот утёс часто называли Кладбищем Неумолимого    Жнеца. На протяжении многих лет люди гибли, падая с этого утёса." \
                "Их было так много, что невозможно сосчитать. Никто из них не выжил, в том числе три Повелителя Божественного уровня, сила которых могла бы привести их на небо."

# Подготовка входных данных с эмоцией
inputs = processor(text_sample, voice_preset=voice_preset, return_attention_mask=True)

# Генерация аудио
audio_array = model.generate(**inputs)
audio_array = audio_array.cpu().numpy().squeeze()

# Сохранение аудио
sample_rate = model.generation_config.sample_rate
name_file = r"output/bark_out_ru_4.wav"
scipy.io.wavfile.write(name_file, rate=sample_rate, data=audio_array)
print(f"Аудио сохранено в файл {name_file}")