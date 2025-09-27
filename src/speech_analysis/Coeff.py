from src.speech_analysis.PatternRecogniser import PatternRecogniser
from src.speech_analysis.IndexCalculator import IndexCalculator

import pandas as pd


class Coeff:
    def __init__(self):
        self.pr = PatternRecogniser()

    def recognise_patterns(self, filepath):
        df = pd.read_csv(filepath, sep='\t')
        interviewee_text = ""
        for line in df.respondent:
            if isinstance(line, str):
                interviewee_text += line
        # print(interviewee_text)
        ic = IndexCalculator()
        result_sents = [
            f'Индекс лексического разнообразия: {str(round(ic.get_lexical_diversity(interviewee_text), 3))}',
            f'Индекс синтаксического разнообразия: {str(round(ic.get_syntactic_diversity(interviewee_text), 3))}',
            f'Индекс удобочитаемости Флеша: {str(round(ic.get_flash_index(interviewee_text), 3))}',
            f'Коэффициент Трейгера: {str(round(ic.get_Treiger_index(interviewee_text), 3))}',
            f'Коэффициент опредмеченности действия: {str(round(ic.get_action_objetification_coefficient(interviewee_text), 3))}',
            f'Доля fixed, parataxis, advmod в тексте: {str(round(ic.get_fpa_coefficient(interviewee_text), 3))}']

        print(result_sents)
