import spacy

class PatternRecogniser:
    def __init__(self):
        self.nlp = spacy.load("local_models/ru_core_news_lg-3.8.0/ru_core_news_lg-3.8.0/ru_core_news_lg/ru_core_news_lg-3.8.0")

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
            if token.pos_ == 'VERB' and 'Act' in token.morph.get('Voice') and 'First' in token.morph.get('Person') and 'Sing' in token.morph.get('Number'):
                matches.append(token.text)
                idxs.append(token.i)
        return (matches, idxs)
    
    def find_plural_active_verbs(self, text):
        doc = self.nlp(text)
        matches = []
        idxs = []
        
        for token in doc:
            if token.pos_ == 'VERB' and 'Act' in token.morph.get('Voice') and 'First' in token.morph.get('Person') and 'Plur' in token.morph.get('Number'):
                matches.append(token.text)
                idxs.append(token.i)
        return (matches, idxs)