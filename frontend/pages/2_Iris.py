import streamlit as st
import pandas as pd 

st.set_page_config(page_title="Ирисы датасет",layout="wide")

@st.cache_data(ttl=10)
def load_data():
    df = pd.read_csv('data/iris.csv')
    print('Датасет успешно загружен!')
    return df

df = load_data()

species_options = df['Species'].unique()

selected_species = st.selectbox(
    label = 'Выберите вид ириса:',
    options=species_options,
    label_visibility='collapsed'
)

filtered_df = df[df['Species'] == selected_species]

st.dataframe(filtered_df)

x_axis = "Id"
y_axis = st.selectbox('Y', df.columns[:-1])

st.scatter_chart(
    filtered_df, 
    x=x_axis, 
    y=y_axis,
    color='Species',
)