import json
import os
from typing import List, Optional
from datetime import datetime

class TTSProgressTracker_min:
    def __init__(self, history_file: str):
        """
        Tracks progress of TTS synthesis and stores history in a JSON file.

        :param history_file: Path to the JSON file for storing progress.
        """
        self.history_file = history_file
        self.progress = self._load_history()  # Load history at initialization

    def _load_history(self) -> dict:
        """Loads the progress history from a JSON file."""
        if os.path.exists(self.history_file):
            with open(self.history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"index": 0}

    def save_progress(self, index: int):
        """Saves the current progress index to the history file."""
        self.progress["index"] = index
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(self.progress, f)

    def get_last_processed_index(self) -> int:
        """Returns the last processed index from history."""
        return self.progress.get("index", 0)

    def reset_progress(self):
        """Resets the progress tracking history."""
        self.progress["index"] = 0
        if os.path.exists(self.history_file):
            os.remove(self.history_file)


class TTSProgressTracker:
    def __init__(self, history_file: str):
        """
        Tracks progress of TTS synthesis and stores history in a JSON file.

        :param history_file: Path to the JSON file for storing progress.
        """
        self.history_file = history_file
        self.progress = self._load_history()

    def _load_history(self) -> dict:
        """Loads the progress history from a JSON file."""
        if os.path.exists(self.history_file):
            with open(self.history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"index": 0, "total": 0, "status": "not_started", "processed_files": [], "errors": []}

    def save_progress(self, index: int, filename: str):
        """Saves the current progress index and processed file info."""
        self.progress["index"] = index
        self.progress["processed_files"].append({
            "index": index,
            "filename": filename,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        self.progress["status"] = "in_progress"
        self._save_to_file()

    def set_total_tasks(self, total: int):
        """Sets the total number of tasks to be processed."""
        self.progress["total"] = total
        self._save_to_file()

    def mark_completed(self):
        """Marks the TTS processing as completed."""
        self.progress["status"] = "completed"
        self._save_to_file()

    def add_error(self, message: str):
        """Logs an error message in the progress file."""
        self.progress["errors"].append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message": message
        })
        self._save_to_file()

    def get_last_processed_index(self) -> int:
        """Returns the last processed index from history."""
        return self.progress.get("index", 0)

    def reset_progress(self):
        """Resets the progress tracking history."""
        self.progress = {"index": 0, "total": 0, "status": "not_started", "processed_files": [], "errors": []}
        self._save_to_file()

    def _save_to_file(self):
        """Saves the progress to a JSON file."""
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(self.progress, f, indent=4)


if __name__ == '__main__':
    # Check TTSProgressTracker_min
    process_dir = "data/checkpoints/history.json"
        # tracker = TTSProgressTracker_min(history_file=process_dir)
        # last_index = tracker.get_last_processed_index()
        # print(f"Last processed index: {last_index}")


        # for i in range(1,5):
        #     tracker.save_progress(i)

        # last_index = tracker.get_last_processed_index()
        # print(f"Last processed index: {last_index}")

        # tracker.reset_progress()
        # last_index = tracker.get_last_processed_index()
        # print(f"Last processed index: {last_index}")

    tracker = TTSProgressTracker(process_dir)
    tracker.reset_progress()
    total_tasks = 100
    tracker.set_total_tasks(total_tasks)
    last_index = tracker.get_last_processed_index()
    print(f"last_index: {last_index}")
    for i in range(last_index, total_tasks):
        filename = f"data/output/test/audio_{i}.wav"
        print(f"Processing {i+1}/{total_tasks}: Generating {filename}...")

        try:
            # Тут должен быть вызов TTS-функции
            # tts_function(text_chunks[i], filename)

            tracker.save_progress(i, filename)
        
        except Exception as e:
            tracker.add_error(str(e)) 

    tracker.mark_completed()

    tracker.reset_progress()
