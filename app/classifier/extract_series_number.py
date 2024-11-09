import pandas as pd
import re

serial_number_regex = r'[CDE](\d{9})|CKM(\d{11})'

# Функция для замены русских букв на английские
def replace_russian_letters(serial):
    translation_table = str.maketrans('АВЕКМНОРСТУХавекмнорстух', 'ABEKMHOPCTYXABEKMHOPCTYX')
    return serial.translate(translation_table)

# Функция для извлечения серийного номера
def extract_serial_number(theme, description):
    # Сначала обрабатываем тему
    tema_with_replaced_letters = replace_russian_letters(theme)
    # Находим серийный номер в теме
    match = re.search(serial_number_regex, tema_with_replaced_letters, re.IGNORECASE)
    
    if match:
        return match.group(0).upper() # Возвращаем найденный серийный номер и приводим к верхнему регистру
    # Если не нашли в "Теме", ищем в "Описание"
    opisanie_with_replaced_letters = replace_russian_letters(description)
    match = re.search(serial_number_regex, opisanie_with_replaced_letters, re.IGNORECASE)

    if match:
        return match.group(0).upper() # Возвращаем найденный серийный номер и приводим к верхнему регистру
    # Если не нашли вообще, возвращаем "Уточнить"
    return "Уточнить"