import streamlit as st
import pandas as pd 
import time 

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix 

st.set_page_config(page_title="ML",layout="wide")

@st.cache_data(ttl=10)
def load_data():
    df = pd.read_csv('data/iris.csv')
    print('Датасет успешно загружен!')
    return df

df = load_data()
st.dataframe(df)

st.divider()

all_features = [f for f in df.columns if f != 'Species']

features = st.multiselect(
    label = 'Выберите признаки для обучения модели:',
    options=all_features
)

if len(features) == 0:
    features = all_features

X = df[features]
y = df['Species']

train_size = st.slider("Размер обучающей выборки:", 0.5, 0.9, 0.7)

if st.button("Обучить модель"):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        train_size=train_size, 
        random_state=None
    )
    model = LogisticRegression(max_iter=100)

    model.fit(X_train, y_train)

    st.session_state.model = model
    st.session_state.X_test = X_test
    st.session_state.y_test = y_test

    time.sleep(10)  # Имитируем длительное обучение модели

    st.success("Модель успешно обучена!")

if st.button("Оценить модель"):
    if 'model' not in st.session_state:
        st.error("Сначала обучите модель!")
    else:
        model = st.session_state.model
        X_test = st.session_state.X_test
        y_test = st.session_state.y_test

        y_pred = model.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)

        st.metric('Точность модели:', f"{acc:.2f}")
        st.write("Матрица ошибок:")
        st.dataframe(cm)


expander = st.expander("debug", expanded=False)
with expander:
    expander.text(st.session_state)
    st.text(features)
