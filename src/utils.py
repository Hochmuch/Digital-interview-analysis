import subprocess

def extract_audio_ffmpeg(video_path, output_audio_path):
    command = [
        'ffmpeg',
        '-i', video_path,
        '-q:a', '0',           # Качество (0 — наивысшее)
        '-map', '0:a',         # Берем только аудио
        output_audio_path
    ]
    subprocess.run(command)
