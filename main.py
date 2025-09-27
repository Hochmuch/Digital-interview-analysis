import argparse
from src.utils import extract_audio_ffmpeg
from src.cli import Cli
from src.audio_processing.AudioProcessor import AudioProcessor

import torch

def main():
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True

    cli = Cli()
    cli.handle()

if __name__ == "__main__":
    main()