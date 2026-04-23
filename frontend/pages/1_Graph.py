import streamlit as st
import numpy as np
import pandas as pd

st.header("Графики в Streamlit")

delta = st.slider("Выберите диапазон для графика:", 1, 10, 2)


# Создание данных для графика
x = np.linspace(0, 10, 100)
y = np.sin(x) + delta

df = pd.DataFrame({
    'x': x, 
    'sin(x)': y
})

# Отображение графика
st.line_chart(df.set_index('x')['sin(x)'])