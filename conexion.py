import streamlit as st
from sqlalchemy import create_engine, URL

url = URL.create(
    "postgresql+psycopg2",
    username=st.secrets["DB_USER"],
    password=st.secrets["DB_PASSWORD"],
    host=st.secrets["DB_HOST"],
    port=int(st.secrets["DB_PORT"]),
    database=st.secrets["DB_NAME"],
)

engine = create_engine(url)
