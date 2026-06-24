import streamlit as st
import requests
import pandas as pd
import sqlite3
from pathlib import Path

st.set_page_config(page_title="Min ML Service", layout="wide")
st.title("🔬 Min ML Service")

# BASE_URL = "http://127.0.0.1:8000"   # Локально
BASE_URL = "http://backend:8000"       # Docker

page = st.sidebar.radio("Навигация", ["Обучение модели", "Загрузка датасета", "История"])

if page == "Обучение модели":
    st.header("Обучение новой модели")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        model_type = st.selectbox("Тип модели", ["logistic", "random_forest"])
        model_name = st.text_input("Название модели", value=f"model_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}")
        
        data_files = [f.name for f in Path("data").glob("*.csv")]
        dataset_filename = st.selectbox("Датасет", data_files if data_files else ["Abalone Dataset.csv"])
        
    with col2:
        target_column = st.text_input("Целевая колонка", value="Rings")
        train_size = st.slider("Размер обучающей выборки (%)", 50, 90, 80) / 100.0

    st.subheader("Гиперпараметры")
    if model_type == "logistic":
        max_iter = st.slider("max_iter", 100, 2000, 1000)
        c_value = st.slider("C", 0.01, 10.0, 1.0)
        hyperparameters = {"max_iter": max_iter, "C": c_value}
    else:
        n_estimators = st.slider("n_estimators", 50, 500, 100)
        max_depth = st.selectbox("max_depth", [None, 5, 10, 15, 20])
        hyperparameters = {"n_estimators": n_estimators, "max_depth": max_depth}

    if st.button("🚀 Запустить обучение", type="primary", use_container_width=True):
        payload = {
            "dataset_filename": dataset_filename,
            "model_type": model_type,
            "model_name": model_name,
            "hyperparameters": hyperparameters,
            "train_size": train_size,
            "target_column": target_column
        }
        
        with st.spinner("Отправка..."):
            try:
                response = requests.post(f"{BASE_URL}/train", json=payload, timeout=30)
                if response.status_code == 200:
                    st.success("✅ Обучение запущено!")
                    st.json(response.json())
                else:
                    st.error(f"Ошибка: {response.text}")
            except Exception as e:
                st.error(f"Не удалось подключиться: {e}")

elif page == "Загрузка датасета":
    st.header("Загрузка датасета")
    uploaded_file = st.file_uploader("CSV файл", type=["csv"])
    if uploaded_file:
        save_path = Path("data") / uploaded_file.name
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Файл {uploaded_file.name} загружен!")
        st.dataframe(pd.read_csv(save_path).head(), use_container_width=True)

else:  
    st.header("История обучений")
    try:
        conn = sqlite3.connect("models.db")
        df = pd.read_sql_query("""
            SELECT id, model_name, model_type, dataset_filename, 
                   target_column, accuracy, created_at 
            FROM training_results 
            ORDER BY created_at DESC
        """, conn)
        conn.close()
        
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            st.success(f"Найдено записей: {len(df)}")
        else:
            st.info("Пока нет записей. Обучите первую модель!")
    except Exception as e:
        st.error(f"Ошибка чтения БД: {e}")
        st.info("Убедитесь, что backend запущен и models.db существует")

st.sidebar.info("Backend: http://localhost:8000/docs")
