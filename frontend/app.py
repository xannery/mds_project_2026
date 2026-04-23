import streamlit as st

st.title("Demo Streamlit!")

name = st.text_input("Введите ваше имя:", placeholder="Студент")
number = st.slider("Выберите число (0-10):", 0, 10, 5)

if st.button("Посчитать квадрат числа"):
    result = number ** 2
    st.success(f"Привет, {name}! Квадрат числа {number} равен {result}.")
    st.balloons()