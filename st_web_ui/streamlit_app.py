import os
import pandas as pd
import streamlit as st
from db import SQLiteManager
from st_styles.base import header, sidebar_title
from create_appeal import config
from create_appeal import create_appeal
from analytics import analytics_page

def appeals():
    """
    Функция для отображения списка обращений с возможностью фильтрации по статусу задачи.
    Загружает данные из базы данных, преобразует даты и позволяет пользователю отфильтровать 
    обращения по статусам.

    Загружает и отображает отфильтрованные данные в таблице с помощью Streamlit.
    """
    header(True)  # Отображение заголовка страницы
    # Загружаем данные из базы данных в DataFrame
    df = st.session_state.db.load_to_dataframe()
    # Преобразуем столбец 'created_at' в формат datetime
    df['created_at'] = pd.to_datetime(df['created_at'], format='mixed')
    # Список возможных статусов задач
    tasks_statuses = ["To Do", "In Progress", "Done", "Reopened", "On Hold"]

    # Мультивыбор для фильтрации по статусу
    selected_statuses = st.multiselect(
        "Select task status to filter by:",
        options=tasks_statuses,
        default=tasks_statuses
    )
    # Фильтрация данных по выбранным статусам
    filtered_df = df[df['status'].isin(selected_statuses)]
    # Отображаем отфильтрованные данные в таблице
    st.dataframe(filtered_df, width=1000, height=600)

def main():
    """
    Основная функция приложения, которая управляет состоянием базы данных, 
    а также маршрутизирует пользователя на страницы: 'Завести обращение', 'Аналитика', 'Обращения'.
    
    При отсутствии базы данных в сессии, она будет инициализирована заново с помощью данных из CSV.
    На боковой панели пользователю предлагается выбрать одну из страниц.
    """
    # Если база данных еще не инициализирована в сессии, создаем новую
    if 'db' not in st.session_state:
        os.remove(config.db_name)  # Удаляем старую базу данных, если она существует
        st.session_state.db = SQLiteManager(config.db_name)  # Инициализируем базу данных
        st.session_state.db.init_db_from_csv(config.init_csv)  # Заполняем базу данных из CSV

    # Отображение заголовка боковой панели
    st.sidebar.markdown(sidebar_title, unsafe_allow_html=True)
    
    # Выбор страницы через боковую панель
    page = st.sidebar.selectbox("Выберите страницу", ["Завести обращение", "Аналитика", "Обращения"])
    
    # Рендеринг соответствующей страницы в зависимости от выбора
    if page == "Завести обращение":
        create_appeal()  # Открытие страницы для создания нового обращения
    elif page == "Аналитика":
        analytics_page()  # Открытие страницы с аналитикой
    elif page == "Обращения":
        appeals()  # Открытие страницы с обращениями

if __name__ == "__main__":
    main()
