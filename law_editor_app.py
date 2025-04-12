# Main Streamlit app
import streamlit as st
from processing.law_processor import process_laws

st.title('부칙 개정 도우미')
search_word = st.text_input('찾을 단어')
replace_word = st.text_input('바꿀 단어')

if st.button('시작'):
    with st.spinner('분석 중...'):
        result = process_laws(search_word, replace_word)
        st.text(result)