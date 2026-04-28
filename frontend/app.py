import streamlit as st

st.title("Demo Streamlit!")

# Ввод данных
name = st.text_input("Введите ваше имя:", placeholder="Студент")

# Слайдер выбора числа
number = st.slider("Выберите число (0-10):", 0, 10, 5)

# Кнопка для выполнения действия
if st.button("Посчитать квадрат числа"):
    result = number ** 2
    st.success(f"Привет, {name}! Квадрат числа {number} равен {result}.")
    st.balloons()
