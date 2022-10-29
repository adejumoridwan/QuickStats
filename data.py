#importing required libraries
import streamlit as st
import pandas as pd


# Allow only .csv and .xlsx files to be uploaded
uploaded_file = st.sidebar.file_uploader("Upload spreadsheet", type=["csv", "xlsx"])

# Check if file was uploaded
if uploaded_file:
    # Check MIME type of the uploaded file
    if uploaded_file.type == "xlsx":
        data = pd.read_excel(uploaded_file, engine = "openpyxl")
    else:
        data= pd.read_csv(uploaded_file)
        

    # Work with the dataframe
    st.dataframe(data)
else:
    st.write("Please Upload a Valid File Format")



