import argparse
from src.audio_processing.AudioProcessor import AudioProcessor
from src.utils import extract_audio_ffmpeg

class Cli:
    def __init__(self):
        self.argparser = argparse.ArgumentParser(description="Средство цифрового анализа интервью. Описание флагов запуска смотрите в разделе help для соответствующих значений.")
        self.group = self.argparser.add_mutually_exclusive_group(required=True)

        # self.group.add_argument("--text", "-t", type=str, help="Путь к текстовому файлу")
        self.group.add_argument("--audio", "-a", type=str, help="Путь к аудиофайлу")
        self.group.add_argument("--video", "-v", type=str, help="Путь к видеофайлу")
        # self.group.add_argument("--other", "-o", type=str, help="Путь к PDF-файлу")

        self.args = self.argparser.parse_args()

    def handle(self):
        if self.args.audio:
            print("Обработка аудио файла", self.args.audio)
            audio_processor = AudioProcessor()
            audio_processor.get_compact_dialog(self.args.audio)

        if self.args.video:
            print("Обработка видео файла", self.args.video)
            extract_audio_ffmpeg(self.args.video, "temp.wav")
            w = AudioProcessor()
            w.get_compact_dialog("temp.wav")