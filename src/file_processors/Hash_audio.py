import audioread
import numpy as np
import hashlib

def audio_hash(file):
    with audioread.audio_open(file) as f:
        raw_data = b"".join(f.read_data())  # Читаем аудиоданные
        return hashlib.md5(raw_data).hexdigest()  # Хешируем

hash1 = audio_hash("/Users/yaao20u291/Pets/output/coqui/Chong_Sheng_Zhi_Jiang_Men_Du_Hou/Chapter_1/Glava_1.mp3")
hash2 = audio_hash("/Users/yaao20u291/Pets/output/coqui/Chong_Sheng_Zhi_Jiang_Men_Du_Hou/Chapter_1/test.wav")

if hash1 == hash2:
    print("Файлы идентичны")
else:
    print("Файлы различаются")
