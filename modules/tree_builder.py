import spacy
from PatternRecogniser import PatternRecogniser

# Загружаем модель
nlp = spacy.load("local_models/ru_core_news_lg-3.8.0/ru_core_news_lg-3.8.0/ru_core_news_lg/ru_core_news_lg-3.8.0")

# Текст для анализа
text = '''То же самое коммуницируешь, скажем, с крупными деятелями, такими как и в Узбекистане, и с чиновниками, и министерствами, так и крупными компаниями. Люди везде одинаковые с точки зрения методологии, подхода общения. Они и здесь тоже самые люди, и тоже самые чиновники, и СЕО, с которыми нужно общаться. И плюс-минус понимание одинаковый подход.'''

text2 = "Лицо, оказывающее помощь."

# Обработка текста
doc = nlp(text2)

# Визуализация дерева зависимостей
#displacy.serve(doc, style="dep")

for token in doc:
    print(f"{token.text:10} POS={token.pos_}  Morph={token.morph}  Dep={token.dep_} Head={token.head}")

pr = PatternRecogniser()
print(pr.find_plural_active_verbs(text2))
print(pr.activity_index_Treiger('''Они и здесь тоже самые люди, и тоже самые чиновники, и СЕО, с которыми нужно общаться.'''))