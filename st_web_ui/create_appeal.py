import json
import requests
import streamlit as st
from configs import StConfig
from st_styles.base import header
from typing import Dict

# Загружаем конфигурационные настройки
config = StConfig()

def print_processed_appeal(response: Dict[str, str]):
    """
    Выводит на экран обработанное обращение, отображая ключи и значения.

    Функция выводит данные обращения, преобразуя ключи в удобочитаемые русские наименования,
    если они указаны в конфигурации. Результат выводится в Streamlit с использованием markdown.

    Аргументы:
        response (Dict[str, str]): Словарь с данными обращения.
    """
    print(response)
    # Проходим по всем ключам в response и выводим их, если они есть в json_key_mapping
    for key, val in response.items():
        if key not in config.json_key_mapping:
            continue
        key = config.json_key_mapping.get(key, key)  # Получаем русское название ключа
        st.markdown(f"**{key}:** {val}")  # Отображаем ключ и значение

def create_appeal():
    """
    Функция для создания обращения, обработки загруженного файла или ввода данных вручную.

    Функция отображает форму для загрузки файлов или ввода информации о теме и описании обращения.
    После получения данных выполняется POST-запрос к API, и полученные результаты выводятся
    на экран и сохраняются в базе данных.

    Если файл загружен, он отправляется на сервер. Если данные введены вручную, они также отправляются на сервер.
    Ответ от сервера сохраняется в состоянии сессии, и выводятся результаты обработки.

    Используется Streamlit для интерфейса пользователя.
    """
    header(only_image=False)  # Отображаем заголовок страницы
    uploaded_file = st.file_uploader("Загрузите CSV, Excel файл", type=["csv", "xlsx", "txt"])  # Загрузка файла

    # Инициализация переменных в сессии, если они не были установлены
    if 'process_btn' not in st.session_state:
        st.session_state.process_btn = False
    if 'response' not in st.session_state:
        st.session_state.response = None

    # Если в сессии есть сохраненный ответ, выводим его
    if st.session_state.response:
        print_processed_appeal(st.session_state.response)

    # Если кнопка обработки не была нажата, показываем поля ввода
    if not st.session_state.process_btn:
        topic_input = st.text_input("Укажите тему обращения") if not uploaded_file else None
        description_input = st.text_area("Опишите вашу проблему") if not uploaded_file else None

        # Если файл загружен или введены текстовые данные, показываем кнопку обработки
        if uploaded_file or (description_input and topic_input):
            if st.button("Обработать"):
                files = {"file": uploaded_file} if uploaded_file else None  # Подготавливаем файл для отправки
                payload = {"topic": topic_input, "description": description_input}  # Подготавливаем данные для запроса

                try:
                    # Отправляем запрос на сервер
                    response = requests.post(config.api_url, data=json.dumps(payload), headers=config.headers)

                    # Если ответ успешный, сохраняем данные и перезагружаем страницу
                    if response.status_code == 200:
                        st.session_state.response = response.json()  # Сохраняем ответ в сессии
                        print(response.json())  # Выводим ответ в консоль
                        st.session_state.db.add_row(response.json())  # Добавляем данные в базу данных
                        st.session_state.process_btn = True  # Устанавливаем флаг обработки
                        st.rerun()  # Перезагружаем страницу
                    else:
                        st.error(f"Ошибка: {response.status_code}. {response.text}")  # Ошибка запроса
                except requests.exceptions.RequestException as e:
                    st.error(f"Ошибка запроса: {e}")  # Обработка исключений запросов
