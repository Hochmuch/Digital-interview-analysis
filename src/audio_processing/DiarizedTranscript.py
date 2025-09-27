class Segment:
    def __init__(self, speaker: str, start: float, end: float, text: str):
        self.speaker = speaker
        self.start = start
        self.end = end
        self.text = text

    def __repr__(self):
        return f"<{self.speaker} [{self.start:.2f} - {self.end:.2f}]: {self.text}>"
    
class DiarizedTranscript:
    def __init__(self):
        self.segments = []
        self.speakers = set()
        self.interviewee = ''

    def add_segment(self, speaker: str, start: float, end: float, text: str):
        segment = Segment(speaker, start, end, text)
        
        if not self.segments or self.segments[-1].speaker != segment.speaker:
            self.segments.append(segment)
        else:
            self.segments[-1].text += segment.text
            self.segments[-1].end = segment.end
        
        self.speakers.add(segment.speaker)