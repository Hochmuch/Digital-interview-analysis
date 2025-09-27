import spacy

class IndexCalculator:
    
    def __init__(self):
        self.nlp = spacy.load("local_models/ru_core_news_lg-3.8.0/ru_core_news_lg-3.8.0/ru_core_news_lg/ru_core_news_lg-3.8.0")
        self.alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz'
        
    def get_lexical_diversity(self, text):
        words_list = []
        words_set = set()
        
        doc = self.nlp(text)
        for sent in doc.sents:
            for token in sent:
                if token.pos_ in ['PUNCT', 'SYM', 'X', 'ADP', 'CCONJ', 'DET', 'NUM', 'PART', 'AUX', 'PRON', 'SCONJ']:
                    continue
                
                lemma = token.lemma_
                words_list.append(lemma)
                words_set.add(lemma)
                
        return len(words_set) / len(words_list)
    
    def get_syntactic_diversity(self, text):
        sentences_count = 0.0
        words_count = 0.0
        
        
        doc = self.nlp(text)
        for sent in doc.sents:
            sentences_count += 1.0
            for token in sent:
                if token.pos_ not in ['PUNCT', 'SYM', 'X']:
                    words_count += 1.0
                    
        return 1.0 - sentences_count / words_count
    
    def get_flash_index(self, text):
        words_count = 0.0
        sentences_count = 0.0
        syllables_count = 0.0
        
        doc = self.nlp(text)
        for sent in doc.sents:
            sentences_count += 1.0
            for token in sent:
                if token.pos_ in ['PUNCT', 'SYM', 'X'] or token.text == '-':
                    continue
                
                for letter in token.text:
                    if letter not in self.alphabet and letter != '-':
                        continue
                
                words_count += 1.0
                for letter in token.text:
                    if letter in letter in 'аоуыэяёюие':
                        syllables_count += 1.0
                        
        return 206.835 - 1.3 * (words_count / sentences_count) - 60.1 * (syllables_count / words_count)

    def get_Treiger_index(self, text):
        doc = self.nlp(text)
        
        verbs_count = 0.0
        adjectives_count = 0.0
        
        for token in doc:
            if token.pos_ == 'VERB':
                verbs_count += 1.0
            elif token.pos_ == 'ADJ':
                adjectives_count += 1.0
        return verbs_count / adjectives_count
    
    def get_action_objetification_coefficient(self, text):
        doc = self.nlp(text)
        
        verbs_count = 0.0
        nouns_count = 0.0
        
        for token in doc:
            if token.pos_ == 'VERB':
                verbs_count += 1.0
            elif token.pos_ == 'NOUN':
                nouns_count += 1.0
        return verbs_count / nouns_count
    
    def get_fpa_coefficient(self, text):
        doc = self.nlp(text)
        
        sentences_count = 0.0
        fpa_count = 0.0
        
        for sent in doc.sents:
            sentences_count += 1.0
            for token in sent:
                if token.dep_ in ['fixed', 'parataxis', 'advmod']:
                    fpa_count += 1.0
                    
        return fpa_count / sentences_count