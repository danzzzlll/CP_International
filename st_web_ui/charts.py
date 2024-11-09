from pydantic_settings import BaseSettings

class StConfig(BaseSettings):
    api_url: str = "your_api_url"
    headers: dict = {"Content-Type": "application/json"}
    json_key_mapping: dict = {
        "topic": "Тема",
        "description": "Описание",
        "device": "Тип устройства",
        "failure_point": "Точка отказа",
        "serial_number": "Серийный номер"
    }

    class Config:
        env_prefix = "APP_"
