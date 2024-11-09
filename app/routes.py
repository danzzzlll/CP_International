from fastapi import APIRouter
from .models import InputData, ResponseData
from .utils import generate_response

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
    response_data = generate_response(
        data.topic,
        data.description
    )
    return response_data  # Возврат сгенерированных данных
