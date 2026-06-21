import streamlit as st
import requests
import pandas as pd
import sqlite3
from pathlib import Path

st.set_page_config(page_title="Min ML Service", layout="wide")
st.title("🔬 Min ML Service - Обучение моделей")

BASE_URL = "http://backend:8000"

page = st.sidebar.radio("Навигация", ["Обучение модели", "Загрузка датасета", "История"])

if page == "Обучение модели":
    st.header("Обучение новой модели")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        model_type = st.selectbox(
            "Тип модели",
            ["logistic", "random_forest"]
        )
        model_name = st.text_input("Название модели", value="my_model_v1")        
    with col2:
        data_files = ["digits"] + [f.name for f in Path("data").glob("*.csv")]
        dataset_filename = st.selectbox("Датасет", data_files)
        
        train_size = st.slider("Размер обучающей выборки (%)", 50, 90, 80) / 100.0

    st.subheader("Гиперпараметры")
    if model_type == "logistic":
        max_iter = st.slider("max_iter", 100, 2000, 1000)
        c_value = st.slider("C (регуляризация)", 0.01, 10.0, 1.0)
        hyperparameters = {"max_iter": max_iter, "C": c_value}
    else:
        n_estimators = st.slider("n_estimators", 50, 500, 100)
        max_depth = st.selectbox("max_depth", [None, 5, 10, 15, 20])
        hyperparameters = {"n_estimators": n_estimators, "max_depth": max_depth}

    if st.button("Запустить обучение", type="primary", use_container_width=True):
        payload = {
            "dataset_filename": dataset_filename,
            "model_type": model_type,
            "model_name": model_name,
            "hyperparameters": hyperparameters,
            "train_size": train_size
        }
        
        with st.spinner("Отправка..."):
            try:
                response = requests.post(f"{BASE_URL}/train", json=payload, timeout=15)
                if response.status_code == 200:
                    st.success("Обучение запущено!")
                    st.json(response.json())
                else:
                    st.error(f"Ошибка {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"Не удалось подключиться к backend: {e}")

elif page == "Загрузка датасета":
    st.header("Загрузка нового датасета")
    uploaded_file = st.file_uploader("CSV файл", type=["csv"])
    
    if uploaded_file:
        save_path = Path("data") / uploaded_file.name
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"Файл **{uploaded_file.name}** загружен!")
        
        try:
            df_preview = pd.read_csv(save_path)
            st.dataframe(df_preview.head(10), use_container_width=True)
        except:
            st.warning("Не удалось прочитать как CSV")

else:  
    st.header("История обучений")
    try:
        conn = sqlite3.connect("models.db")
        df = pd.read_sql_query("""
            SELECT id, model_name, model_type, dataset_filename, 
                   accuracy, created_at 
            FROM training_results 
            ORDER BY created_at DESC
        """, conn)
        conn.close()
        
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Пока нет записей")
    except Exception as e:
        st.info("База данных ещё не инициализирована")
