import pandas as pd
import plotly.express as px
import streamlit as st
from st_styles.base import (
    header,
    get_color_discrete_sequence
)
from utils import generate_pdf_and_download


def analytics_page():
    header(True)
    df = pd.read_csv('data/date_status_data.csv')
    st.markdown(f"**Суммарное кол-во записей:** {len(df)}")
    color_discrete_sequence = get_color_discrete_sequence()
    
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce').dt.date
    dates = st.date_input("Выберете даты", value=[df['created_at'].min(), df['created_at'].max()])
    try:
        start_date, end_date = dates
        df_filtered = df[(df['created_at'] >= start_date) & (df['created_at'] <= end_date)]

        st.markdown(f"**Отображается кол-во записей за выбранный период:** {len(df_filtered)}")

        failure_point_count = df_filtered['Точка отказа'].value_counts().reset_index()
        failure_point_count.columns = ['Точка отказа', 'Количество']
        fig2 = px.pie(
            failure_point_count,
            names='Точка отказа',
            values='Количество',
            title='Количество обращений Точка отказа',
            color_discrete_sequence=color_discrete_sequence
        )
        st.plotly_chart(fig2)

        topic_count = df_filtered['Тип оборудования'].value_counts().reset_index()
        topic_count.columns = ['Тип оборудования', 'Количество']
        fig1 = px.bar(
            topic_count,
            x='Тип оборудования',
            y='Количество',
            title='Количество обращений по темам',
            color_discrete_sequence=color_discrete_sequence
        )
        st.plotly_chart(fig1)

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

        day_point_count = df_filtered.groupby(
            [df_filtered['created_at'],
             'Тип оборудования']
            ).size().reset_index(name='Количество')
        fig4 = px.line(
            day_point_count,
            x='created_at',
            y='Количество',
            color='Тип оборудования',
            title='Кол-во обращений по типу обращения',
            color_discrete_sequence=color_discrete_sequence
        )
        fig4.update_xaxes(type='category')
        fig4.update_layout(xaxis_title='Дата', yaxis_title='Кол-во', legend_title='Тип оборудования')
        st.plotly_chart(fig4)

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
        plots = [fig2, fig1, fig3, fig4, fig5]

        if st.button("Сформировать отчет"):
            pdf_buffer = generate_pdf_and_download(plots)
            st.download_button(
                label="Скачать отчет",
                data=pdf_buffer,
                file_name="plots.pdf",
                mime="application/pdf"
            )
    except:
        pass
