import spacy

from .IndexCalculator import IndexCalculator


class PatternRecogniser:
    def __init__(self):
        self.nlp = spacy.load(
            "local_models/ru_core_news_lg-3.8.0/ru_core_news_lg-3.8.0/ru_core_news_lg/ru_core_news_lg-3.8.0")

    def split_sentences(self, text: str):
        doc = self.nlp(text)
        return [sent.text.strip() for sent in doc.sents]

    def find_modal_need_verbs(self, text):
        """
        Находит выражения общего долженствования вроде "надо сделать",
        "нужно применять" и т.п.
        Ищет наречия (надо, нужно) с зависимым инфинитивом.
        """

        modal_necessity_words = ['нужно', 'необходимо', 'надо', 'следует']

        doc = self.nlp(text)
        matches = []
        idxs = []

        for token in doc:
            if token.text.lower() in modal_necessity_words:
                for child in token.children:
                    if child.pos_ == 'VERB' and 'Inf' in child.morph.get('VerbForm') and child.dep_ == 'csubj':
                        matches.append(f"{token.text} {child.text}")
                        idxs.append((min(token.i, child.i), max(token.i, child.i)))
        return (matches, idxs)

    def find_passive_expressions(self, text):
        """
        Находит клаузальные подлежащие в пассивных конструкциях.
        Например: "Что он был уволен, было ожидаемо."
        """
        doc = self.nlp(text)
        matches = []
        idxs = []

        for token in doc:
            if token.pos_ == 'AUX' and 'Part' in token.head.morph.get('VerbForm'):
                matches.append([token.text.lower(), token.head.text.lower()])
                idxs.append((min(token.i, token.head.i), max(token.i, token.head.i)))
        return (matches, idxs)

    def find_singular_active_verbs(self, text):
        doc = self.nlp(text)
        matches = []
        idxs = []

        for token in doc:
            if token.pos_ == 'VERB' and 'Act' in token.morph.get('Voice') and 'First' in token.morph.get(
                    'Person') and 'Sing' in token.morph.get('Number'):
                matches.append(token.text)
                idxs.append(token.i)
        return (matches, idxs)

    def find_plural_active_verbs(self, text):
        doc = self.nlp(text)
        matches = []
        idxs = []

        for token in doc:
            if token.pos_ == 'VERB' and 'Act' in token.morph.get('Voice') and 'First' in token.morph.get(
                    'Person') and 'Plur' in token.morph.get('Number'):
                matches.append(token.text)
                idxs.append(token.i)
        return (matches, idxs)

    # def recognise_patterns(self, filepath):
    #     dt = self.get_compact_dialog(filepath)
    #     interviewee = self.recognize_interviewee(dt)
    #
    #     interviewee_text = ''
    #     for segment in dt.segments:
    #         if segment.speaker == interviewee:
    #             if interviewee_text == '':
    #                 interviewee_text = segment.text
    #             else:
    #                 interviewee_text += '\n'
    #                 interviewee_text += segment.text
    #
    #     ic = IndexCalculator()
    #
    #     result_sents = [
    #         'Индекс лексического разнообразия: ' + str(round(ic.get_lexical_diversity(interviewee_text), 3)),
    #         'Индекс синтаксического разнообразия: ' + str(round(ic.get_syntactic_diversity(interviewee_text), 3)),
    #         'Индекс удобочитаемости Флеша: ' + str(round(ic.get_flash_index(interviewee_text), 3)),
    #         'Коэффициент Трейгера: ' + str(round(ic.get_Treiger_index(interviewee_text), 3)),
    #         'Коэффициент опредмеченности действия: ' + str(
    #             round(ic.get_action_objetification_coefficient(interviewee_text), 3)),
    #         'Доля fixed, parataxis, advmod в тексте: ' + str(round(ic.get_fpa_coefficient(interviewee_text), 3))]
    #
    #     pdf = PDFHighlighter("interview.pdf")
    #
    #     for segment in dt.segments:
    #         doc = self.pr.nlp(segment.text)
    #
    #         if segment.speaker != interviewee:
    #             for sent in doc.sents:
    #                 colors = ['black' for i in range(len(sent))]
    #                 pdf.render_sentence(sent, colors)
    #             pdf.newline()
    #             continue
    #
    #         for sent in doc.sents:
    #
    #             colors = ['black' for i in range(len(sent))]
    #
    #             modal_need_verbs = self.pr.find_modal_need_verbs(sent.text.strip())
    #             for expr in modal_need_verbs[1]:
    #                 for i in range(expr[0], expr[1] + 1):
    #                     colors[i] = 'blue'
    #
    #             # print(self.pr.find_modal_need_verbs(sent.text.strip()))
    #             passive_expressions = self.pr.find_passive_expressions(sent.text.strip())
    #             for expr in passive_expressions[1]:
    #                 for i in range(expr[0], expr[1] + 1):
    #                     colors[i] = 'red'
    #
    #             plural_active_verbs = self.pr.find_plural_active_verbs(sent.text.strip())
    #             for expr in plural_active_verbs[1]:
    #                 colors[expr] = 'green'
    #
    #             singular_active_verbs = self.pr.find_singular_active_verbs(sent.text.strip())
    #             for expr in singular_active_verbs[1]:
    #                 colors[expr] = 'yellow'
    #
    #             pdf.render_sentence(sent, colors)
    #         pdf.newline()
    #
    #     pdf.create_result()
    #     for sent in result_sents:
    #         pdf.render_result_sentence(sent)
    #     pdf.save()
