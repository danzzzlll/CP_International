import streamlit as st
from create_appeal import create_appeal
from analytics import analytics_page



import pandas as pd
import streamlit as st
from st_styles.base import header

def appeals():
    header(True)
    df = pd.read_csv('data/date_status_data.csv')
    tasks_statuses = ["To Do", "In Progress", "Done", "Reopened", "On Hold"]

    selected_statuses = st.multiselect(
        "Select task status to filter by:",
        options=tasks_statuses,
        default=tasks_statuses
    )
    filtered_df = df[df['status'].isin(selected_statuses)]
    st.dataframe(filtered_df, width=1000, height=600)

def main():
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
