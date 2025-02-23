import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../inc/VALL_EX')))

from utils.generation import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
from IPython.display import Audio

# download and load all models
preload_models()

# generate audio from text
text_prompt = """
            Bark is available in the 🤗 Transformers library from version 4.31.0 onwards, requiring minimal dependencies and additional packages. Steps to get started:
            """
audio_array = generate_audio(text_prompt)

# save audio to disk
write_wav("output/vallex_generation.wav", SAMPLE_RATE, audio_array)

# play text in notebook
Audio(audio_array, rate=SAMPLE_RATE)
