import streamlit as st
from modules import text_anonymizer, image_anonymizer, pdf_anonymizer

st.set_page_config(page_title="SentriX", layout="centered", initial_sidebar_state="auto")

st.markdown("""
    <style>
    body, .stApp {
        background-color: #1d1c30;
        color: #ffffff;
    }
    label, .css-1fv8s86, .css-1aumxhk, .css-1nw4l3l {  /* классы для label и input */
        color: #ffffff !important;
    }
    /* Кнопки с черным текстом на белом фоне */
    button {
        color: #000000 !important;
        background-color: #ffffff !important;
        font-weight: bold;
    }
    /* Селектбокс: чёрный текст на белом фоне */
    div[role="listbox"] {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("SentriX — Локальная анонимизация данных")

option = st.selectbox("Что вы хотите анонимизировать?", ["Текст", "Изображение", "PDF"])

if option == "Текст":
    input_text = st.text_area("Введите текст для анонимизации")
    if st.button("Анонимизировать текст"):
        result = text_anonymizer.anonymize_text(input_text)
        st.text_area("Результат", result, height=200)
elif option == "Изображение":
    uploaded_image = st.file_uploader("Загрузите изображение", type=["jpg", "jpeg", "png"])
    if uploaded_image:
        result_img = image_anonymizer.anonymize_image(uploaded_image)
        st.image(result_img, caption="Анонимизированное изображение")
elif option == "PDF":
    uploaded_pdf = st.file_uploader("Загрузите PDF", type=["pdf"])
    if uploaded_pdf:
        path = pdf_anonymizer.anonymize_pdf(uploaded_pdf)
        with open(path, "rb") as f:
            st.download_button("📥 Скачать анонимизированный PDF", f, file_name="anonymized.pdf")
