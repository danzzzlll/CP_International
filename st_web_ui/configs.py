from typing import Dict
from pydantic_settings import BaseSettings


class StConfig(BaseSettings):
    """
    Класс для конфигурации настроек приложения.

    Этот класс используется для загрузки и хранения настроек приложения с использованием
    библиотеки Pydantic для работы с настройками и валидаторами. Все параметры, указанные в этом классе,
    будут загружены из переменных окружения или файлов конфигурации, если таковые имеются.

    Атрибуты:
        api_url (str): URL API для генерации данных.
        db_name (str): Имя файла базы данных.
        init_csv (str): Путь к CSV файлу, содержащему начальные данные.
        headers (Dict[str, str]): Заголовки для HTTP запросов.
        json_key_mapping (Dict[str, str]): Сопоставление ключей JSON для преобразования данных.
    """
    
    # URL API для генерации данных
    api_url: str = "http://localhost:8000/generate"
    
    # Имя файла базы данных
    db_name: str = "appeals.db"
    
    # Путь к CSV файлу с начальными данными
    init_csv: str = "data/date_status_data.csv"
    
    # Заголовки для HTTP запросов
    headers: Dict[str, str] = {
        "Content-Type": "application/json"
    }
    
    # Сопоставление ключей JSON с их русскими названиями
    json_key_mapping: Dict[str, str] = {
        "topic": "Тема обращения",
        "description": "Описание",
        "device": "Тип оборудования",
        "failure_point": "Точка отказа",
        "serial_number": "Серийный номер"
    }
