import spacy
from collections import Counter

nlp = spacy.load("local_models/ru_core_news_lg-3.8.0/ru_core_news_lg-3.8.0/ru_core_news_lg/ru_core_news_lg-3.8.0")

active_words = {
    "делать", "достигать", "действовать", "запускать", "организовать",
    "подготовить", "решить", "реализовать", "контролировать", "подписать",
    "работать", "двигаться", "стремиться", "успевать", "улучшать"
}

reflective_words = {
    "думать", "размышлять", "анализировать", "ощущать", "чувствовать",
    "предполагать", "осознавать", "понимать", "переживать", "наблюдать",
    "иногда", "может быть", "возможно", "постепенно", "размеренно"
}

def classify_text(text):
    doc = nlp(text.lower())
    
    lemmas = [token.lemma_ for token in doc if token.is_alpha]
    lemma_counts = Counter(lemmas)
    
    active_count = sum(lemma_counts[word] for word in active_words)
    reflective_count = sum(lemma_counts[word] for word in reflective_words)
    
    total_count = active_count + reflective_count

    if total_count == 0:
        return "Неопределено", active_count, reflective_count
    
    if active_count > reflective_count:
        return "Активный стиль", active_count, reflective_count
    else:
        return "Рефлексивный стиль", active_count, reflective_count

active_text = """Сегодня я решил быстро организовать команду для запуска нового проекта. Мы провели планёрку, распределили задачи и начали работу."""
reflective_text = """Иногда я задумываюсь о том, как всё происходит. После долгих размышлений приходит понимание сути событий."""

for t in [active_text, reflective_text]:
    result, a_count, r_count = classify_text(t)
    print(f"Текст: {t[:50]}...")
    print(f"Результат: {result} (Активные: {a_count}, Рефлексивные: {r_count})\n")
