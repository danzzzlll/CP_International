import pandas as pd
import datetime
import plotly.express as px
import streamlit as st
from st_styles.base import (
    header,
    get_color_discrete_sequence
)
from utils import generate_pdf_and_download


def analytics_page():
    """
    Страница аналитики с визуализацией данных.

    Эта функция отвечает за загрузку данных из базы данных, фильтрацию по выбранным пользователем датам
    и отображение различных графиков (pie, bar, line) для анализа данных. Также включает кнопку для
    формирования и скачивания отчета в формате PDF.

    Процесс:
        1. Загрузка данных из базы данных в DataFrame.
        2. Фильтрация данных по выбранному диапазону дат.
        3. Создание различных визуализаций для анализа.
        4. Опция для скачивания отчета в PDF формате с графиками.
    """
    # Отображение заголовка страницы
    header(True)

    # Загрузка данных из базы данных
    df = st.session_state.db.load_to_dataframe()

    # Получение палитры цветов для графиков
    color_discrete_sequence = get_color_discrete_sequence()

    # Преобразование столбца created_at в формат даты
    df['created_at'] = pd.to_datetime(df['created_at'], format='mixed').dt.date

    # Получение диапазона дат для фильтрации
    dates = st.date_input("Выберете даты", value=[df['created_at'].min(), df['created_at'].max()])

    try:
        # Фильтрация данных по выбранному диапазону дат
        start_date, end_date = dates
        df_filtered = df[(df['created_at'] >= start_date) & (df['created_at'] <= end_date)]

        # Отображение количества записей за выбранный период
        st.markdown(f"**Отображается кол-во записей за выбранный период:** {len(df_filtered)}")

        # График круговой диаграммы по точкам отказа
        failure_point_count = df_filtered['failure_point'].value_counts().reset_index()
        failure_point_count.columns = ['Точка отказа', 'Количество']
        fig2 = px.pie(
            failure_point_count,
            names='Точка отказа',
            values='Количество',
            title='Количество обращений Точка отказа',
            color_discrete_sequence=color_discrete_sequence
        )
        st.plotly_chart(fig2)

        # График столбчатой диаграммы по типам оборудования
        topic_count = df_filtered['device'].value_counts().reset_index()
        topic_count.columns = ['Тип оборудования', 'Количество']
        fig1 = px.bar(
            topic_count,
            x='Тип оборудования',
            y='Количество',
            title='Количество обращений по темам',
            color_discrete_sequence=color_discrete_sequence
        )
        st.plotly_chart(fig1)

        # График линейной диаграммы по количеству обращений в течение времени
        day_count = df_filtered.groupby(df_filtered['created_at']).size().reset_index(name='Количество')
        day_count = day_count.sort_values('created_at')
        fig3 = px.line(
            day_count,
            x='created_at',
            y='Количество',
            title='Кол-во обращений в течение времени',
            color_discrete_sequence=color_discrete_sequence
        )
        fig3.update_xaxes(type='category')
        fig3.update_layout(xaxis_title='Дата', yaxis_title='Кол-во')
        st.plotly_chart(fig3)

        # График линейной диаграммы по количеству обращений по типам устройств
        day_point_count = df_filtered.groupby(
            [df_filtered['created_at'],
             'device']
        ).size().reset_index(name='Количество')
        fig4 = px.line(
            day_point_count,
            x='created_at',
            y='Количество',
            color='device',
            title='Кол-во обращений по типу обращения',
            color_discrete_sequence=color_discrete_sequence
        )
        fig4.update_xaxes(type='category')
        fig4.update_layout(xaxis_title='Дата', yaxis_title='Кол-во', legend_title='Тип оборудования')
        st.plotly_chart(fig4)

        # График столбчатой диаграммы по статусам обращений
        topic_count = df_filtered['status'].value_counts().reset_index().sample(frac=1)
        topic_count.columns = ['Статус обращения', 'Количество']
        fig5 = px.bar(
            topic_count,
            x='Статус обращения',
            y='Количество',
            title='Статусы задач',
            color_discrete_sequence=color_discrete_sequence
        )
        st.plotly_chart(fig5)

        # Список всех графиков
        plots = [fig2, fig1, fig3, fig4, fig5]

        # Кнопка для формирования отчета
        if st.button("Сформировать отчет"):
            pdf_buffer = generate_pdf_and_download(plots)
            st.download_button(
                label="Скачать отчет",
                data=pdf_buffer,
                file_name="plots.pdf",
                mime="application/pdf"
            )
    except:
        # Обработка ошибок, если они возникнут
        pass
