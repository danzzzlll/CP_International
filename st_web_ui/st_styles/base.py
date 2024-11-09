import streamlit as st

def header(only_image:bool=False):
    if not only_image:
        st.markdown(
        '<div class="image-container">\
        <img src="https://sila.ru/sites/all/themes/sila/images/logo-1.svg"\
        alt="Header Image" width="100" height="100"></div>'
        ,unsafe_allow_html=True
        )
        st.markdown("""
            <style>
                .subheader {
                    padding-top: 20px;
                    font-size: 20px;
                    color: #777;
                    text-align: center;
                    margin-top: -10px;
                }
                .image-container {
                    text-align: center;
                    margin-top: 20px;
                }
            </style>
            <div class="subheader">
                Загрузите файл в формате csv, Excel, или текст обращения напрямую через форму для последующей классификации
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(
        '<div class="image-container">\
        <img src="https://sila.ru/sites/all/themes/sila/images/logo-1.svg"\
        alt="Header Image" width="100" height="100"></div>'
        ,unsafe_allow_html=True
        )
        st.markdown("""
            <style>
                .subheader {
                    padding-top: 20px;
                    font-size: 20px;
                    color: #777;
                    text-align: center;
                    margin-top: -10px;
                }
                .image-container {
                    text-align: center;
                    margin-top: 20px;
                }
            </style>
            <div class="subheader">
                Аналитика по текущим обращениям
            </div>
        """, unsafe_allow_html=True)


def get_color_discrete_sequence():
    return [
            "#0068c9",
            "#83c9ff",
            "#ff2b2b",
            "#ffabab",
            "#29b09d",
            "#7defa1",
            "#ff8700",
            "#ffd16a",
            "#6d3fc0",
            "#d5dae5",
        ]

def appeal_info_style():
     st.markdown(
            """
            <style>
                .key { font-weight: bold; color: #4CAF50; }
                .value { font-size: 16px; color: #2C3E50; }
                .separator { border-top: 1px solid #BDC3C7; margin: 10px 0; }
                .ticket-container { background-color: #f9f9f9; padding: 20px; border-radius: 10px; }
                .section-title { font-size: 18px; font-weight: bold; color: #34495E; }
            </style>
            """, unsafe_allow_html=True
        )


sidebar_title = """
        <head>
            <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
        </head>
        <div style="text-align: center; font-family: 'Roboto', sans-serif; padding-bottom: 30px;">
            <span style="font-size: 44px; font-weight: bold; background: linear-gradient(90deg, #32CD32, #00FF7F); -webkit-background-clip: text; color: transparent;">Грин</span>
            <span style="font-size: 44px; font-weight: bold; background: linear-gradient(90deg, #1E90FF, #00BFFF); -webkit-background-clip: text; color: transparent;"> МИСИС</span>
        </div>
    """