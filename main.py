import argparse
import modules.media_handler as mh
from modules.logic import Worker

def main():
    argparser = argparse.ArgumentParser(description="Средство цифрового анализа интервью. Описание флагов запуска смотрите в разделе help для соответствующих значений.")
    group = argparser.add_mutually_exclusive_group(required=True)
    
    group.add_argument("--text", "-t", type=str, help="Путь к текстовому файлу")
    group.add_argument("--audio", "-a", type=str, help="Путь к аудиофайлу")
    group.add_argument("--video", "-v", type=str, help="Путь к видеофайлу")
    group.add_argument("--other", "-o", type=str, help="Путь к PDF-файлу")
    
    args = argparser.parse_args()
    
    if args.text:
        print("Обработка текстового файла", args.text)
        w = Worker()
    if args.audio:
        print("Обработка аудио файла", args.audio)
        w = Worker()
        w.recognise_patterns(args.audio)
        
    if args.video:
        print("Обработка видео файла", args.video)
        mh.extract_audio_ffmpeg(args.video, "temp.wav")
        w = Worker()
        w.recognise_patterns(args.video)
        
    if args.other:
        print("Обработка pdf файла")
        w = Worker()

if __name__ == "__main__":
    main()