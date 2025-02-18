import torch
from TTS.api import TTS
# print(TTS().list_models())

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# List available 🐸TTS models
# print(TTS.tts().list_modesls())

# Initialize TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
# tts = TTS("tts_models/multilingual/multi-dataset/your_tts").to(device)

# List speakers
print(tts.speakers)

# text_prompt = """
#             Bark is available in the 🤗 Transformers library from version 4.31.0 onwards, requiring minimal dependencies and additional packages. Steps to get started:
#             """
text_prompt = "Заоблачный утёс Божественной Тайной горы был самым пугающим из четырех смертоносных мест Континента Лазурного Облака." \
                "Этот утёс часто называли Кладбищем Неумолимого    Жнеца. На протяжении многих лет люди гибли, падая с этого утёса." \
                "Их было так много, что невозможно сосчитать. Никто из них не выжил, в том числе три Повелителя Божественного уровня, сила которых могла бы привести их на небо."

# speakers = ['Claribel Dervla', 'Daisy Studious', 'Gracie Wise', 'Tammie Ema', 'Alison Dietlinde', 'Ana Florence', 'Annmarie Nele', 'Asya Anara', 'Brenda Stern', 'Gitta Nikolina', 'Henriette Usha', 'Sofia Hellen', 'Tammy Grit', 'Tanja Adelina', 'Vjollca Johnnie', 'Andrew Chipper', 'Badr Odhiambo', 'Dionisio Schuyler', 'Royston Min', 'Viktor Eka', 'Abrahan Mack', 'Adde Michal', 'Baldur Sanjin', 'Craig Gutsy', 'Damien Black', 'Gilberto Mathias', 'Ilkin Urbano', 'Kazuhiko Atallah', 'Ludvig Milivoj', 'Suad Qasim', 'Torcull Diarmuid', 'Viktor Menelaos', 'Zacharie Aimilios', 'Nova Hogarth', 'Maja Ruoho', 'Uta Obando', 'Lidiya Szekeres', 'Chandra MacFarland', 'Szofi Granger', 'Camilla Holmström', 'Lilya Stainthorpe', 'Zofija Kendrick', 'Narelle Moon', 'Barbora MacLean', 'Alexandra Hisakawa', 'Alma María', 'Rosemary Okafor', 'Ige Behringer', 'Filip Traverse', 'Damjan Chapman', 'Wulf Carlevaro', 'Aaron Dreschner', 'Kumar Dahl', 'Eugenio Mataracı', 'Ferran Simen', 'Xavier Hayasaka', 'Luis Moray', 'Marcos Rudaski']

# print(len(speakers))

# for speaker in speakers:
#     name_file_path = f"output/coqui_out_{speaker}.wav"
# # TTS to a file, use a preset speaker
#     tts.tts_to_file(
#     text=text_prompt,
#     speaker=speaker,
#     language="ru",
#     file_path=name_file_path
#     )
#     print(f"Аудио сохранено в файл {name_file_path}")

# print(f"Все готово, Слушай дурик")