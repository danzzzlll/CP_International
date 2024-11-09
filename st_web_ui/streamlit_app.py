from create_appeal import create_appeal
from analytics import analytics_page
from db import SQLiteManager
import pandas as pd
import streamlit as st
import os
from st_styles.base import header
from create_appeal import config

def appeals():
    header(True)
    df = st.session_state.db.load_to_dataframe()
    df['created_at'] = pd.to_datetime(df['created_at'], format='mixed')
    tasks_statuses = ["To Do", "In Progress", "Done", "Reopened", "On Hold"]

    selected_statuses = st.multiselect(
        "Select task status to filter by:",
        options=tasks_statuses,
        default=tasks_statuses
    )
    filtered_df = df[df['status'].isin(selected_statuses)]
    st.dataframe(filtered_df, width=1000, height=600)

def main():
    if 'db' not in st.session_state:
        os.remove(config.db_name)
        st.session_state.db = SQLiteManager(config.db_name)
        st.session_state.db.init_db_from_csv(config.init_csv)
    sidebar_title = """
        <head>
            <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
        </head>
        <div style="text-align: center; font-family: 'Roboto', sans-serif; padding-bottom: 30px;">
            <span style="font-size: 44px; font-weight: bold; background: linear-gradient(90deg, #32CD32, #00FF7F); -webkit-background-clip: text; color: transparent;">Грин</span>
            <span style="font-size: 44px; font-weight: bold; background: linear-gradient(90deg, #1E90FF, #00BFFF); -webkit-background-clip: text; color: transparent;"> МИСИС</span>
        </div>
    """

    st.sidebar.markdown(sidebar_title, unsafe_allow_html=True)
    page = st.sidebar.selectbox("Выберите страницу", ["Завести обращение", "Аналитика", "Обращения"])
    if page == "Завести обращение":
        create_appeal()
    elif page == "Аналитика":
        analytics_page()
    elif page == "Обращения":
        appeals()

if __name__ == "__main__":
    main()
