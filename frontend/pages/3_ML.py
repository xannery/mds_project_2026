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

col_1, col_2 = st.columns(2)

with col_1:
    all_features = [f for f in df.columns if f != "Species"]

    features = st.multiselect(
        "Select features",
        all_features
    )

    if len(features) == 0:
        features = all_features

    X = df[features]
    y = df["Species"]

    train_size = st.slider("Train size", 0.5, 0.9, 0.7)

    if st.button("Train"):
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            train_size=train_size,
            random_state=None
        )

        model = LogisticRegression()

        model.fit(X_train, y_train)

        st.session_state.model = model
        st.session_state.X_test = X_test
        st.session_state.y_test = y_test

        # time.sleep(10)

        st.success("Model trained")


with col_2:
    if st.button("Evaluate model"):
        if 'model' not in st.session_state:
            st.error("Сначала обучите модель!")
        else:
            model = st.session_state.model
        X_test = st.session_state.X_test
        y_test = st.session_state.y_test

        y_pred = model.predict(X_test)

        acc = accuracy_score(y_test, y_pred)

        st.metric(label="Точность модели", value=f"{acc:.2f}")

        st.metric(label='Accuracy', value=round(acc, 3))

        cm = confusion_matrix(y_test, y_pred)

        st.subheader("Confusion Matrix")
        st.dataframe(cm)

        st.bar_chart(pd.Series(y_pred).value_counts())

    
expander = st.expander("debug", expanded=False)
with expander:
    expander.text(st.session_state)
    st.text(features)

