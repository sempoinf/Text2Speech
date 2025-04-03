import os
import re
from itertools import islice

from file_processors.text_utils import TextChunker
from Coqui_tss.Coqui_speech import CoquiTTS
from file_processors.tts_tracker import TTSProgressTracker
from file_processors.audio_merger import AudioPostProcessor

# at the end delete cache??

class Application():
    def __init__(self, output_dir: str, mask_name: str, history_file: str):
        """
        Main class that manages text processing, TTS synthesis, and progress tracking.

        :param output_dir: Directory for saving output audio files.
        :param base_filename: Base name for generated files.
        :param history_file: Path to the JSON file for tracking progress.
        """
        self.output_dir = output_dir
        self.base_filename = mask_name
        self.text_chunker = TextChunker()
        self.tts = CoquiTTS(gpu=True)
        self.tracker = TTSProgressTracker(history_file)
        self.merger = AudioPostProcessor(directory=output_dir, base_filename=mask_name, output_format='mp3') # name want to get from parsing url or text

        os.makedirs(output_dir, exist_ok=True)
    
    def fetch_text(self, source: str) -> str:
        """
        Fetches text from a file or a URL.

        :param source: Path to a text file or a URL.
        :return: Extracted text.
        """
        if source.startswith(("http://", "https://")):
            text_chunks = self.text_chunker.from_url(url=source, split=True)
            print(f"Reading data from url finished!")
        elif os.path.isfile(source):
            text_chunks = self.text_chunker.from_file(file_path=source, split=True)
            print(f"Reading data from file finished!")
        else:
            print("Invalid source provided. Must be a valid file path or URL.")
            return ""
        
        if not text_chunks:
            print("Error: No text retrieved.")
            return []

        # Ensure cache directory exists
        cache_dir = r"data/cache/"
        os.makedirs(cache_dir, exist_ok=True)

        self.cache_file = os.path.join(cache_dir, text_chunks[0]+'.txt')
        self.text_chunker.save_chunks_to_file(text_chunks, file_path=self.cache_file)
        print(f"Work with input - Complete!")
        return text_chunks
    

    def synthesize_text(self, chunks: str):
        """
        Synthesizes text using TTS while tracking progress.

        :param text: Input text to be processed.
        """
        if not chunks:
            print("No chunks to process.")
            return

        # history_dir = "/data/history/"
        # os.makedirs(history_dir, exist_ok=True)

        self.tracker.set_total_tasks(len(chunks))
        start_index = self.tracker.get_last_processed_index()
        if start_index >= len(chunks):
            print("Start index exceeds the number of chunks.")
            return

        for i, segment in enumerate(islice(chunks, start_index, None), start=1):
            output_path = os.path.join(self.output_dir, f"{self.base_filename}_{i}.mp3")
            try:
                self.tts.synthesize(segment, output_path, speaker= 'Baldur Sanjin', language="ru")
                self.tracker.save_progress(i, output_path)
                print(f"Complete for chunk: {i}")
            except Exception as e:
                self.tracker.add_error(str(e))
                print(f"Error processing chunk {i}: {e}")
                break  # Stop processing if an error occurs

        self.tracker.mark_completed()
        print(f"Complete for all chunks")
        # self.tracker.reset_progress()

    def audio_merger(self):
        """
        Mb here init class?
        """
        fin_audio_path = self.merger.merge_audio()
        print(f"File merged: {fin_audio_path}")

if __name__ == "__main__":
    # chunker = TextChunker()
    # # .pdf, .txt, .docx
    # path_input_f = r'data/input/name.txt' 
    # test_txt = chunker.from_file(file_path=path_input_f, split=True)

    # path_cach_f = r'/data/cache/name.txt'
    # test_txt = chunker.save_chunks_to_file(text=test_txt, file_path=path_cach_f, split=False)

    # tts = CoquiTTS(gpu=True)
    # # model_name = "tts_models/multilingual/multi-dataset/xtts_v2"

    # # stopped on 73 fragment
    # for i, segment in enumerate(islice(test_txt, 0, None), start=1):
    #     print(i)
    #     # print(len(segment))
    #     path_save_file = f"output/coqui/Chong_Sheng_Zhi_Jiang_Men_Du_Hou/Glava_1_{i}.wav"
    #     tts.synthesize(str(segment), path_save_file, speaker= 'Baldur Sanjin', language="ru")
    #     print(f"Complete for fragment {i}")
    # print(f"Complete for all")

    # # processor = AudioPostProcessor(directory="output", base_filename="tts_output", output_format="mp3")
    # # fin_audio_path = processor.merge_audio()
    # # print(f"File merged: {fin_audio_path}")


    # output_dir = "processed_audio"
    # base_filename = "speech"

    # tts_processor = TTSProcessor(dummy_tts, output_dir, base_filename)
    # tts_processor.process_texts(text_chunks)


    # source = r'data/input/test_text.txt'
    # out_dir = r'data/output/test'
    # mask = r'test'
    # his_f = r'data/history/history.json'
    # api = Application(output_dir=out_dir, base_filename=mask, history_file=his_f)
    # api.tracker.reset_progress()
    # chunks = api.fetch_text(source)
    # print(chunks)
    # api.synthesize_text(chunks)
    # api.audio_merger()
    # api.tracker.reset_progress()

    source = r'https://ranobelib.me/ru/28369--the-rebirth-of-the-malicious-empress-of-military-lineage/read/v1/c1'
    out_dir = r'/Users/yaao20u291/Pets/Text2Speech/data/output/coqui/Chong_Sheng_Zhi_Jiang_Men_Du_Hou/Chapter_1'
    mask = r'Chapter_1'
    his_f = r'data/history/history.json'
    api = Application(output_dir=out_dir, mask_name=mask, history_file=his_f)
    # api.tracker.reset_progress()
    # chunks = api.fetch_text(source)
    # api.synthesize_text(chunks)
    api.audio_merger()
