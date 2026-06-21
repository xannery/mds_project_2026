import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Графики",layout="wide")

if 'delta' not in st.session_state:
    st.session_state.delta = 3

st.header("График синусоида в Streamlit")

with st.sidebar:
    st.session_state.delta = st.slider("Выберите диапазон для графика:", 1, 20, st.session_state.delta)

# Разделение страницы на две колонки
col_1, col_2 = st.columns(2)


# Создание данных для графика
x = np.linspace(0, 10, 100)
y = np.sin(x) + st.session_state.delta

df = pd.DataFrame({
    'x': x, 
    'sin(x)': y
})

# Первая колонка - график  
with col_1:
    st.subheader("График синусоиды")    
    col_1.line_chart(df.set_index('x')['sin(x)'])
    st.subheader("Аналитика графика")
    st.write("Максимальное значение синусоиды:", df['sin(x)'].max())
    st.write("Минимальное значение синусоиды:", df['sin(x)'].min())
    st.write("Среднее значение синусоиды:", df['sin(x)'].mean()) 
    st.dataframe(df)

st.info("График обновляется при изменении ползунка в сайдбаре")

expander = st.expander("debug", expanded=True)

expander.text(st.session_state)
