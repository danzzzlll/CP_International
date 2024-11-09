import streamlit as st
from create_appeal import create_appeal
from analytics import analytics_page

def main():
    page = st.sidebar.selectbox("Выберите страницу", ["Завести обращение", "Аналитика"])
    if page == "Завести обращение":
        create_appeal()
    elif page == "Аналитика":
        analytics_page()

if __name__ == "__main__":
    main()
