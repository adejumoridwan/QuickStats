#importing required libraries
import streamlit as st
import pandas as pd


# Allow only .csv and .xlsx files to be uploaded
uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel File", type=["csv", "xlsx"])

# Check if file was uploaded
if uploaded_file:
    # Check MIME type of the uploaded file
    if uploaded_file.type == "xlsx":
        data = pd.read_excel(uploaded_file, engine = "openpyxl")
    else:
        data= pd.read_csv(uploaded_file)
        

    Data, Descriptive = st.tabs(["Data", "Descriptive"])

    Data.dataframe(data)

    Descriptive.header("Descriptive Statistics")

    Descriptive.table(data.describe())
    

#retun message if no file is uploaded
else:
    st.subheader("Please Upload a Valid File Format")




