import streamlit as st
import pandas as pd 

st.set_page_config(page_title="Ирисы датасет",layout="wide")

@st.cache_data(ttl=10)
def load_data():
    df = pd.read_csv('data/iris.csv')
    print('Датасет успешно загружен!')
    return df

df = load_data()

st.dataframe(df)