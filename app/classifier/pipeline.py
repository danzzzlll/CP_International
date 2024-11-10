from .tfidf.model import ClassificationModel  # Импортируем модель классификации на основе TF-IDF
from typing import Tuple  # Импортируем для указания возвращаемого типа
from .extract_series_number import extract_serial_number  # Импортируем функцию для извлечения серийного номера
from .bert.bert import TypeBert  # Импортируем класс BERT для классификации
from .llm.inference_llm import get_priority  # Импортируем функцию для определения приоритета

# Функция для извлечения серийного номера и классификации с использованием модели TF-IDF
def extract_and_classify(theme: str, description: str) -> Tuple[str, str, str]:
    # Объединяем тему и описание в один текст
    full_text = theme + " " + description
    
    # Инициализируем модель для классификации типа
    type_model = ClassificationModel(mode="type")
    # Классифицируем текст и определяем его тип
    type_ = type_model.get_class(full_text)
    
    # Инициализируем модель для классификации признака stop_dot
    stop_dot_model = ClassificationModel(mode="stop_dot")
    # Извлекаем серийный номер из темы и описания
    serial_number_ = extract_serial_number(theme=theme, description=description)
    # Классифицируем текст и определяем значение stop_dot
    stop_dot_ = stop_dot_model.get_class(full_text)
    
    # Определяем приоритет на основе темы и описания
    priority_ = get_priority(theme, description)
    
    # Возвращаем тип, stop_dot, серийный номер и приоритет
    return type_, stop_dot_, serial_number_, priority_

# Функция для извлечения серийного номера и классификации с использованием модели BERT
def bert_extract_and_classify(theme: str, description: str) -> Tuple[str, str, str]:
    # Объединяем тему и описание в один текст
    full_text = theme + " " + description
    
    # Инициализируем BERT модель для классификации типа
    type_model = TypeBert(mode="type")
    # Классифицируем текст и определяем его тип
    type_ = type_model(full_text)
    
    # Инициализируем BERT модель для классификации признака stop_dot
    stop_dot_model = TypeBert(mode="stop_dot")
    # Извлекаем серийный номер из темы и описания
    serial_number_ = extract_serial_number(theme=theme, description=description)
    # Классифицируем текст и определяем значение stop_dot
    stop_dot_ = stop_dot_model(full_text)
    
    # Определяем приоритет на основе темы и описания
    priority_ = get_priority(theme, description)
    
    # Возвращаем тип, stop_dot, серийный номер и приоритет
    return type_, stop_dot_, serial_number_, priority_
