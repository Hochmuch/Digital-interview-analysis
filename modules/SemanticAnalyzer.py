import json
import spacy
import pymorphy3

class SemanticAnalyzer:
    def __init__(self):
        self.categories = dict()
        self.nlp = spacy.load("local_models/ru_core_news_lg-3.8.0/ru_core_news_lg-3.8.0/ru_core_news_lg/ru_core_news_lg-3.8.0")
        self.morph = pymorphy3.MorphAnalyzer()

    def load_from_file(self, file_path):
        self.categories = dict()
        with open(file_path, 'r', encoding='utf-8') as file:
            self.categories = json.load(file)

    def save_to_file(self, file_path):
        
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(self.categories, file, ensure_ascii=False, indent=4)
        except:
            print('Файл не существует.')

    def add_category(self, category_name, words):
        self.categories[category_name] = words

    def add_words_to_category(self, category_name, words):
        if category_name not in self.categories:
            self.categories[category_name] = []
            
        words = set(words)
        self.categories[category_name] = set(self.categories[category_name])
        self.categories[category_name] |= words
        self.categories[category_name] = list(self.categories[category_name])

    def get_words_in_category(self, category_name):
        return self.categories.get(category_name, [])

    def get_all_categories(self):
        return list(self.categories.keys())

    def remove_category(self, category_name):
        if category_name in self.categories:
            self.categories.pop(category_name)

    def remove_words_from_category(self, category_name, words):
        words = set(words)
        self.categories[category_name] = set(self.categories[category_name])
        self.categories[category_name] -= words
        self.categories[category_name] = list(self.categories[category_name])
        
    def analyze(self, text, normalize=False):
        doc = self.nlp(text)
        count = dict()
        tokens_count = 0.0
                
        for category in self.categories:
            count[category] = 0.0
        
        for sent in doc.sents:
            for token in sent:
                if token.pos_ in ['NUM', 'PROPN', 'PUNCT', 'SYM', 'X']:
                    continue
                
                lemma = token.lemma_
                
                tokens_count += 1.0
                for category in self.categories:
                    if lemma in self.categories[category]:
                        count[category] += 1.0
                        
        if normalize:
            for category in count:
                if tokens_count == 0:
                    return None
                else:
                    count[category] = count[category] / tokens_count
                    
        return count
                       


sa = SemanticAnalyzer()
verbs_thinking = [
    "думать", "размышлять", "анализировать", "осмысливать", "предполагать",
    "подумать", "поразмыслить", "проанализировать", "осмыслить", "предположить",
    
    "планировать", "рассчитывать", "исследовать", "обсуждать", "моделировать",
    "спланировать", "рассчитать", "обсудить", "смоделировать",
    
    "рассуждать", "понимать", "обдумывать", "представлять", "учитывать",
    "порассуждать", "понять", "обдумать", "представить", "учесть",
    
    "проектировать", "полагать", "воображать", "рассматривать", "идентифицировать",
    "спроектировать", "вообразить", "рассмотреть",
    
    "классифицировать", "осмысливать", "оценивать", "формулировать", "прогнозировать",
    "осмыслить", "оценить", "сформулировать", "спрогнозировать",
    
    "осознавать", "решать", "просчитывать", "рассчитывать", "считывать"
    "осознать", "решить", "просчитать", "рассчитать", "считать"
]
sa.add_category('Глаголы размышления', verbs_thinking)
sa.save_to_file("test.json")

z = '''Обязан
Должен
Никогда
Невозможно
Бесспорно
Абсолютно
Всегда
Везде
Никогда
Никто
Ничто
Несомненно
Безусловно
Неизбежно
Неотложно
Категорически
Обязательно
Совершенно
Неуклонно
Неопровержимо
Именно
Решительно
Совсем
Точно
Навсегда
Неизменно
Непременно
Всеобъемлюще
Однозначно
Решительно
Категорически
Исключительно
Обязательно
Непререкаемо
Неотъемлемо
Постоянно
Несомненно
Всецело
Безоговорочно
Предельно'''.split()

z = [word.lower() for word in z]
sa.add_category('А-экспрессия', z)
sa.save_to_file('data/categories.json')