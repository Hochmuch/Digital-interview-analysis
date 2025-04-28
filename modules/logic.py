import whisper
from pyannote.audio import Pipeline
import torch
from modules.DiarizedTranscript import DiarizedTranscript
from modules.PatternRecogniser import PatternRecogniser
from modules.pdf_writer import PDFHighlighter
from modules.IndexCalculator import IndexCalculator


class Worker:
    def __init__(self):
        self.transcriber = whisper.load_model("turbo")
        self.diarizer = Pipeline.from_pretrained("local_models/pyannote_local/config.yaml")
        self.diarizer.to(torch.device("cuda"))
        self.pr = PatternRecogniser()
        
    def transcribe(self, filepath):
        return self.transcriber.transcribe(filepath, word_timestamps=True)
    
    def diarize(self, filepath):
        return self.diarizer(filepath, num_speakers=2)
    
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
        
        f = open('out.txt', 'w')
        
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
        
        f.close()        
        
        return dt
    
    def recognize_interviewee(self, dt):
        speaker_word_count = dict()
        
        for speaker in dt.speakers:
            speaker_word_count[speaker] = 0
            
        for segment in dt.segments:
            doc = self.pr.nlp(segment.text)
            speaker_word_count[segment.speaker] += sum([1 for token in doc if not token.is_punct and not token.is_space])
            
        return max(speaker_word_count)
    
    def recognise_patterns(self, filepath):
        dt = self.get_compact_dialog(filepath)
        interviewee = self.recognize_interviewee(dt)
        
        interviewee_text = ''
        for segment in dt.segments:
            if segment.speaker == interviewee:
                if interviewee_text == '':
                    interviewee_text = segment.text
                else:
                    interviewee_text += '\n'
                    interviewee_text += segment.text
                    
        ic = IndexCalculator()
        
        result_sents = ['Индекс лексического разнообразия: ' + str(round(ic.get_lexical_diversity(interviewee_text), 3)),
                 'Индекс синтаксического разнообразия: ' + str(round(ic.get_syntactic_diversity(interviewee_text), 3)),
                 'Индекс удобочитаемости Флеша: ' + str(round(ic.get_flash_index(interviewee_text), 3)),
                 'Коэффициент Трейгера: ' + str(round(ic.get_Treiger_index(interviewee_text), 3)),
                 'Коэффициент опредмеченности действия: ' + str(round(ic.get_action_objetification_coefficient(interviewee_text), 3)),
                 'Доля fixed, parataxis, advmod в тексте: ' + str(round(ic.get_fpa_coefficient(interviewee_text), 3))]
        
        
        pdf = PDFHighlighter("interview.pdf")
        
        for segment in dt.segments:
            doc = self.pr.nlp(segment.text)
            
            if segment.speaker != interviewee:
                for sent in doc.sents:
                    colors = ['black' for i in range(len(sent))]
                    pdf.render_sentence(sent, colors)
                pdf.newline()
                continue
            
            for sent in doc.sents:
                
                colors = ['black' for i in range(len(sent))]
                
                modal_need_verbs = self.pr.find_modal_need_verbs(sent.text.strip())
                for expr in modal_need_verbs[1]:
                    for i in range(expr[0], expr[1] + 1):
                        colors[i] = 'blue'
                        
                #print(self.pr.find_modal_need_verbs(sent.text.strip()))
                passive_expressions = self.pr.find_passive_expressions(sent.text.strip())
                for expr in passive_expressions[1]:
                    for i in range(expr[0], expr[1] + 1):
                        colors[i] = 'red'
                
                plural_active_verbs = self.pr.find_plural_active_verbs(sent.text.strip())
                for expr in plural_active_verbs[1]:
                    colors[expr] = 'green'
                
                singular_active_verbs = self.pr.find_singular_active_verbs(sent.text.strip())
                for expr in singular_active_verbs[1]:
                    colors[expr] = 'yellow'
                        
                pdf.render_sentence(sent, colors)
            pdf.newline()
        
        pdf.create_result()
        for sent in result_sents:
            pdf.render_result_sentence(sent)
        pdf.save()
                
        
#w = Worker()
#w.recognise_patterns('обрезанное_аудио5.wav')
#print(w.pr.find_modal_need_verbs('''Они и здесь тоже самые люди, и тоже самые чиновники, и СЕО, с которыми нужно общаться.'''))