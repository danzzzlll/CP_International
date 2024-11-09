import json
import requests
import streamlit as st
from configs import StConfig
from st_styles.base import header
from typing import Dict

config = StConfig()

def print_processed_appeal(response: Dict[str, str]):
    print(response)
    for key, val in response.items():
        if key not in config.json_key_mapping:
            continue
        key = config.json_key_mapping.get(key, key)
        st.markdown(f"**{key}:** {val}")

def create_appeal():
    header(only_image=False)
    uploaded_file = st.file_uploader("Загрузите CSV, Excel файл", type=["csv", "xlsx", "txt"])
    if 'process_btn' not in st.session_state:
        st.session_state.process_btn = False
    if 'response' not in st.session_state:
        st.session_state.response = None
    if st.session_state.response:
        print_processed_appeal(st.session_state.response)

    if not st.session_state.process_btn:
        topic_input = st.text_input("Укажите тему обращения") if not uploaded_file else None
        description_input = st.text_area("Опишите вашу проблему") if not uploaded_file else None
        if uploaded_file or (description_input and topic_input):
            if st.button("Обработать"):
                files = {"file": uploaded_file} if uploaded_file else None
                payload = {"topic": topic_input, "description": description_input}
                try:
                    response = requests.post(config.api_url, data=json.dumps(payload), headers=config.headers)
                    if response.status_code == 200:
                        st.session_state.response = response.json()
                        print(response.json())
                        st.session_state.db.add_row(response.json())
                        st.session_state.process_btn = True
                        st.rerun()
                    else:
                        st.error(f"Ошибка: {response.status_code}. {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Ошибка запроса: {e}")
