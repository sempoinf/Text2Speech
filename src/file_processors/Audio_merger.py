import os
import re
from pydub import AudioSegment


class AudioPostProcessor:
    def __init__(self, directory, base_filename, output_format="wav"):
        self.directory = directory
        self.base_filename = base_filename
        self.output_format = output_format.lower()
        self.supported_formats = ["wav", "mp3", "ogg"]

        if self.output_format not in self.supported_formats:
            raise ValueError(f"Unsupported format: {self.output_format}. Use one of {self.supported_formats}")

    def _get_audio_files(self):
        """ Get and Sort Files """
        pattern = re.compile(rf"{re.escape(self.base_filename)}_(\d+)\.(wav|mp3|ogg)$")
        # print(pattern)
        files = [f for f in os.listdir(self.directory) if pattern.match(f)]
        # print(files)
        # Sort files
        files.sort(key=lambda x: int(re.search(r"_(\d+)\.", x).group(1)))
        # print(files)
        return [os.path.join(self.directory, f) for f in files]

    def normalize_audio(self, audio, target_dBFS=-15.0):
        """ Normalize audio to a target dBFS level """
        return audio.apply_gain(target_dBFS - audio.dBFS)

    def merge_audio(self):
        """ Merged in one file """
        files = self._get_audio_files()
        # print(files)
        if not files:
            raise FileNotFoundError("No matching audio files found.")

        # combined = AudioSegment.empty()
        combined = AudioSegment.silent(duration=0)
        for file in files:
            # input(file)
            audio = AudioSegment.from_file(file)
            audio = self.normalize_audio(audio)
            combined += audio

        output_path = os.path.join(self.directory, f"{self.base_filename}.{self.output_format}")
        combined.export(output_path, format=self.output_format)
        return output_path


if __name__ == "__main__":
    path_files = r"data/output/coqui/Chong_Sheng_Zhi_Jiang_Men_Du_Hou"
    mask_name = r"Glava_1"
    
    processor = AudioPostProcessor(directory=path_files, base_filename=mask_name, output_format="mp3")
    fin_audio_path = processor.merge_audio()
    print(f"File merged: {fin_audio_path}")
