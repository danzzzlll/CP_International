from pydantic import BaseModel

class InputData(BaseModel):
    """
    Модель для входных данных.

    Атрибуты:
        topic (str): Тема, о которой идет речь.
        description (str): Описание, связанное с темой.
    """
    topic: str  # Тема
    description: str  # Описание

class ResponseData(BaseModel):
    """
    Модель для ответа с дополнительной информацией.

    Атрибуты:
        created_at (str): Дата и время создания записи.
        status (str): Статус ответа.
        topic (str): Тема, о которой идет речь.
        description (str): Описание, связанное с темой.
        device (str): Устройство, связанное с ошибкой или проблемой.
        failure_point (str): Точка сбоя или проблема, связанная с устройством.
        serial_number (str): Серийный номер устройства.
    """
    created_at: str  # Дата и время создания
    status: str  # Статус
    topic: str  # Тема
    description: str  # Описание
    device: str  # Устройство
    failure_point: str  # Точка сбоя
    serial_number: str  # Серийный номер устройства
    priority: str
