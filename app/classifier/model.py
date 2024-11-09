import pymorphy3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from .keywords import KeyWords

morph = pymorphy3.MorphAnalyzer()

class ClassificationModel:
    def __init__(self, morph=morph, mode="type"): # two modes: 'type' 'stop_dot'
        self.morph=morph
        self.mode = mode
        if mode == 'type':
            self.keywords = KeyWords.type_keywords
        else:
            self.keywords = KeyWords.stop_dot_keywords

    def preprocess_and_lemmatize(self, text):
        """
        Функция для предобработки и лемматизации текста.
        Удаляет спецсимволы, лемматизирует слова.
        """
        # Приведение текста к нижнему регистру и удаление спецсимволов, кроме букв, цифр и пробелов
        text = re.sub(r'[^а-яА-Я0-9\s]', '', text.lower())
        # Лемматизация слов
        lemmatized_words = [self.morph.parse(word)[0].normal_form for word in text.split()]
        return ' '.join(lemmatized_words)
    
    def count_matching_tokens(self, text, keywords):
        """
        Подсчитывает количество совпадений токенов из текста с ключевыми словами.
        """
        text_tokens = set(text.split())
        return sum(1 for word in keywords if word in text_tokens)
    
    def categorize_text(self, text, threshold=0.5):
        """
        Функция для определения категории текста на основе заданных ключевых слов и порогового значения.
        
        Parameters:
        - text (str): текст обращения.
        - stop_dot_keywords (dict): словарь, где ключи - категории, а значения - массивы ключевых слов.
        - threshold (float): пороговое значение (от 0 до 1) для определения соответствия категории.

        Returns:
        - list: Список категорий, к которым относится текст.
        """
        # Лемматизация текста обращения
        text = self.preprocess_and_lemmatize(text)
        
        # Лемматизация ключевых слов для каждой категории
        lemmatized_keywords = {category: [self.preprocess_and_lemmatize(word) for word in keywordes]
                            for category, keywordes in self.keywords.items()}
        
        # Соединение всех лемматизированных ключевых слов из словаря
        all_keywords = [' '.join(keywordes) for keywordes in lemmatized_keywords.values()]
        categories = list(lemmatized_keywords.keys())

        # Создание TF-IDF матрицы
        tfidf = TfidfVectorizer()
        tfidf_matrix = tfidf.fit_transform([text] + all_keywords)
        
        # Расчет косинусного сходства
        cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
        
        # Учет пересечения токенов для усиления точности
        token_overlap_scores = [
            self.count_matching_tokens(text, lemmatized_keywords[category]) / len(lemmatized_keywords[category])
            for category in categories
        ]
        
        # Усреднение косинусного сходства и пересечения токенов
        combined_scores = [(cos_sim + token_overlap) / 2 for cos_sim, token_overlap in zip(cosine_sim, token_overlap_scores)]
        
        # Определение категорий, которые соответствуют порогу
        matching_categories = [categories[i] for i, score in enumerate(combined_scores) if score >= threshold]
        
        return matching_categories
    
    
    def get_class(self, text):
        if self.mode == "type":
            print('Using default value for type')
            common_word = "Ноутбук"
        else:
            print('Using default value for point failure')
            common_word = "Материнская плата"

        try:
            category = self.categorize_text(text, threshold=0.07)[0]
        except:
            category = common_word
            pass
        return category
