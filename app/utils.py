import datetime 

def generate_response(topic: str, description: str):
    """
    Генерация ответа на основе темы и описания.

    Эта функция принимает тему и описание, а затем создает и возвращает словарь
    с информацией о создании, статусе, устройстве, точке сбоя и серийном номере.

    Аргументы:
        topic (str): Тема, о которой идет речь.
        description (str): Описание, связанное с темой.

    Возвращаемое значение:
        dict: Словарь с полями:
            - created_at (str): Дата и время создания записи.
            - status (str): Статус ответа.
            - topic (str): Тема, о которой идет речь.
            - description (str): Описание, связанное с темой.
            - device (str): Устройство, связанное с ошибкой.
            - failure_point (str): Точка сбоя.
            - serial_number (str): Серийный номер устройства.
    """
    # Получение текущей даты и времени
    current_date = str(datetime.datetime.now())
    
    # Возвращение сгенерированного словаря
    return {
        "created_at": current_date,  # Время создания
        "status": "To Do",  # Статус
        "topic": topic,  # Тема
        "description": description,  # Описание
        "device": "Ноутбук",  # Устройство
        "failure_point": "Блок питания",  # Точка сбоя
        "serial_number": "C223100360"  # Серийный номер
    }
