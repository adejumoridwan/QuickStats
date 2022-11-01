#importing required libraries
import streamlit as st
import pandas as pd


st.sidebar.header("Upload Data")

# Allow only .csv and .xlsx files to be uploaded
uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel File", type=["csv", "xlsx"])

# Check if file was uploaded
if uploaded_file:
    # Check MIME type of the uploaded file
    if uploaded_file.type == "xlsx":
        data = pd.read_excel(uploaded_file, engine = "openpyxl")
    else:
        data= pd.read_csv(uploaded_file)

    Data, Descriptive, Visualization, Inferential = st.tabs(["Data", "Descriptive","Visualization","Inferential"])
    
    Data.dataframe(data)

    Descriptive.header("Descriptive Statistics")

    Descriptive.table(data.describe())

    data_variables = data.columns

    st.sidebar.header("Visualization Controls")

    plot_type = st.sidebar.selectbox("Select Plot Type", ["BarChart","Histogram","Boxplot","Scatterplot","Lineplot"])

    x_axis = st.sidebar.selectbox('Select X-axis', data_variables)

    y_axis = st.sidebar.selectbox('Select Y-axis', data_variables)

    group = st.sidebar.selectbox('Select Group', data_variables)

    

    

#retun message if no file is uploaded
else:
    st.subheader("Please Upload a Valid File Format")




