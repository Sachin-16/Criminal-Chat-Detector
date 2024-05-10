#for run : streamlit run app.py
import streamlit as st
import matplotlib.pyplot as plt
#import preprocessor, helper
import seaborn as sns


st.title("Criminal Chat Detector")
st.sidebar.title("Analyze Your Chats")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")