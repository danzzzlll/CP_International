import json
import requests
import pandas as pd
import streamlit as st
from configs import StConfig
from st_styles.base import header, appeal_info_style
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
    # Проходим по всем ключам в response и выводим их, если они есть в json_key_mapping
    with st.container():
        appeal_info_style()
        st.markdown('<div class="ticket-container">', unsafe_allow_html=True)
        # if response['device'] == "СХД":
        #     response['priority'] = "Высокая"
        # elif response['device'] == "Ноутбук" or response['device'] == 'Сервер':
        #     response['priority'] = "Средняя"

        for key, val in response.items():
            if key not in config.json_key_mapping and key != 'priority':
                continue
            if key == 'priority':
                key = 'Приоритет'
            else:
                key = config.json_key_mapping.get(key, key)  # Get the Russian name if available
            # Create a nice separator line after each ticket entry
            st.markdown(f'<div class="section-title">{key}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="key"> </div><div class="value">{val}</div>', unsafe_allow_html=True)
            st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

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
    if uploaded_file:
        if uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            # Чтение Excel файла
            df = pd.read_excel(uploaded_file)
        elif uploaded_file.type == "text/csv":
            # Чтение CSV файла
            df = pd.read_csv(uploaded_file)

        # Проверка необходимых колонок
        if "Тема" in df.columns and "Описание" in df.columns:
            payloads = df[["Тема", "Описание"]].to_dict(orient="records")
            st.write(f"Загруженные данные: {payloads}")
        else:
            st.error('Файл должен содержать столбцы "Тема" и "Описание".')

    # Если кнопка обработки не была нажата, показываем поля ввода
    if not st.session_state.process_btn:
        topic_input = st.text_input("Укажите тему обращения") if not uploaded_file else None
        description_input = st.text_area("Опишите вашу проблему") if not uploaded_file else None

        # Если файл загружен или введены текстовые данные, показываем кнопку обработки
        if uploaded_file or (description_input and topic_input):
            if uploaded_file or (description_input and topic_input):
                if st.button("Обработать"):
                    # Если был загружен файл обрабатываем его построчно
                    if uploaded_file:
                        for payload in payloads:
                            try:
                                #Отправка каждой строки на api service
                                response = requests.post(config.api_url, data=json.dumps(payload), headers=config.headers)

                                # Обработка запроса
                                if response.status_code == 200:
                                    st.session_state.response = response.json()  # Сохранение в сессию
                                    to_db = dict(response.json())
                                    del to_db['priority']
                                    st.session_state.db.add_row(to_db)  # Добавлени в БД
                                    st.session_state.process_btn = True
                                else:
                                    st.error(f"Ошибка: {response.status_code}. {response.text}")
                            except requests.exceptions.RequestException as e:
                                st.error(f"Ошибка запроса: {e}")
                    
                    # Обработка ручного ввода
                    elif topic_input and description_input:
                        payload = {"topic": topic_input, "description": description_input}
                        try:
                            response = requests.post(config.api_url, data=json.dumps(payload), headers=config.headers)

                            if response.status_code == 200:
                                st.session_state.response = response.json()
                                st.session_state.db.add_row(response.json())  # Добавление в БД
                                st.session_state.process_btn = True
                                st.rerun()
                            else:
                                st.error(f"Ошибка: {response.status_code}. {response.text}")
                        except requests.exceptions.RequestException as e:
                            st.error(f"Ошибка запроса: {e}")

