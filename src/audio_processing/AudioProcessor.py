import whisper
from pyannote.audio import Pipeline
import torch
from .DiarizedTranscript import DiarizedTranscript


class AudioProcessor:
    def __init__(self):
        self.transcriber = whisper.load_model("turbo")
        self.diarizer = Pipeline.from_pretrained("local_models/pyannote_local/config.yaml")
        self.diarizer.to(torch.device("cuda"))

    def transcribe(self, filepath):
        return self.transcriber.transcribe(filepath, word_timestamps=True)

    def diarize(self, filepath):
        return self.diarizer(filepath, num_speakers=2)  # сюда передавать данные через .env

    def get_compact_dialog(self, filepath):
        dialog = list(self.diarize(filepath).itertracks(yield_label=True))
        new_dialog = []

        whisper_segments = self.transcribe(filepath)['segments']

        for expression in dialog:
            turn, _, speaker = expression

            if turn.end - turn.start < 0.3:
                continue

            if len(new_dialog) == 0 or new_dialog[-1][0] != speaker:
                new_dialog.append([speaker, turn.start, turn.end])
            else:
                new_dialog[-1][2] = turn.end

        dt = DiarizedTranscript()

        indent = 0.4
        i = 0

        with open('out.txt', 'w') as f:  # тут не хардкодить
            for expression in whisper_segments:
                if expression['start'] >= new_dialog[i][1] - indent and expression['end'] <= new_dialog[i][2] + indent:
                    f.write(f"{expression['text']} {new_dialog[i][0]}\n")
                    dt.add_segment(new_dialog[i][0], expression['start'], expression['end'], expression['text'])
                else:
                    i += 1
                    if i >= len(new_dialog):
                        break
                    f.write(f"{expression['text']} {new_dialog[i][0]}\n")
                    dt.add_segment(new_dialog[i][0], expression['start'], expression['end'], expression['text'])

        return dt
