from typing import Dict
from pydantic_settings import BaseSettings


class StConfig(BaseSettings):
    api_url: str = "http://localhost:8000/generate"
    headers: Dict[str, str] = {
        "Content-Type": "application/json"
    }
    json_key_mapping: Dict[str, str] = {
        "topic": "Тема обращения",
        "description": "Описание",
        "device": "Тип оборудования",
        "failure_point": "Точка отказа",
        "serial_number": "Серийный номер"
    }