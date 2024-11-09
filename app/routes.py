import datetime
from fastapi import APIRouter
from .models import InputData, ResponseData
from .classifier.pipeline import extract_and_classify
router = APIRouter()

@router.post("/generate", response_model=ResponseData)
async def generate(data: InputData):
    """
    Обработчик POST-запроса для генерации ответа.

    Этот эндпоинт принимает входные данные с темой и описанием, генерирует ответ
    с помощью функции `generate_response` и возвращает данные в формате `ResponseData`.

    Аргументы:
        data (InputData): Входные данные, содержащие тему и описание.

    Возвращаемое значение:
        ResponseData: Сгенерированные данные, включающие информацию о создании, статусе,
        устройстве, точке сбоя и серийном номере.
    """
    # Генерация ответа с использованием функции generate_response
    device, failure_point, serial_number  = extract_and_classify(
        theme=data.topic,
        description=data.description
    )
    current_date = str(datetime.datetime.now())
    return {
        "created_at": current_date,  # Время создания
        "status": "To Do",  # Статус
        "topic": data.topic,  # Тема
        "description": data.description,  # Описание
        "device": device,  # Устройство
        "failure_point": failure_point,  # Точка сбоя
        "serial_number": serial_number  # Серийный номер
    }
