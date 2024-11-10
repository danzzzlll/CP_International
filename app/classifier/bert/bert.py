import logging
from ..keywords import KeyWords  # Импортируем ключевые слова
from sentence_transformers import SentenceTransformer  # Импортируем модель Sentence Transformer для создания эмбеддингов
from sklearn.metrics.pairwise import cosine_similarity  # Импортируем функцию для расчета косинусного сходства

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Задаем имя модели
model_name = "deepvk/USER-bge-m3"

# Класс для работы с BERT моделью
class TypeBert:
    def __init__(self, mode="type"):  # 2 режима: "type" и "stop_dot"
        # Загружаем модель SentenceTransformer
        self.model = SentenceTransformer(model_name)
        logger.info("Model Loaded!!!")  # Логируем загрузку модели
        # Выбираем ключевые слова в зависимости от режима
        if mode == "type":
            self.keywords = KeyWords.type_keywords
        else:
            self.keywords = KeyWords.stop_dot_keywords
        logger.info(f'Use {mode} keywords')  # Логируем выбранный режим ключевых слов

    # Метод для создания эмбеддингов ключевых слов
    def make_keywords_embed(self):
        type_keywords_embedded = {}
        for key in self.keywords.keys():
            # Генерируем эмбеддинги для каждого ключевого слова
            type_keywords_embedded[key] = [self.model.encode(self.keywords[key])]
        return type_keywords_embedded

    # Метод для создания эмбеддингов текста
    def make_text_embed(self, text):
        return self.model.encode([text], normalize_embeddings=True)

    # Метод для поиска ближайшего ключевого слова по сходству с текстом
    def find_nearest(self, text):
        # Генерируем эмбеддинг для заданного текста
        element = self.make_text_embed(text=text)
        max_sim = 0  # Инициализируем максимальное сходство
        ans = ''  # Переменная для хранения ближайшего ключевого слова
        type_keywords_embedded = self.make_keywords_embed()  # Получаем эмбеддинги ключевых слов
        for key in type_keywords_embedded.keys():
            # Рассчитываем косинусное сходство между эмбеддингом ключевого слова и текста
            sim = cosine_similarity(type_keywords_embedded[key][0], element).flatten()
            # Если сходство выше текущего максимума, обновляем максимальное сходство и ближайшее слово
            if sim[0] > max_sim:
                ans = key
                max_sim = sim[0]
        return ans

    # Метод вызова объекта как функции, для поиска ближайшего ключевого слова
    def __call__(self, text):
        return self.find_nearest(text=text)
