#importing required libraries
import streamlit as st
import pandas as pd
import plotly.express as px


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

    Data, Descriptive, Visualization = st.tabs(["Data", "Descriptive","Visualization"])
    
    Data.dataframe(data)

    Descriptive.header("Descriptive Statistics")

    Descriptive.table(data.describe())

    data_variables = data.columns

    st.sidebar.header("Visualization Controls")

    plot_type = st.sidebar.selectbox("Select Plot Type", ("BarChart","Histogram","Boxplot","Scatterplot","Lineplot"))

    if plot_type == "BarChart":
        x_axis = st.sidebar.selectbox('Select X-axis', data_variables)

        group = st.sidebar.selectbox('Select Group', data_variables)

        if data[x_axis].dtype == 'object':
            bar_fig = px.bar(data, x=x_axis, color = group, barmode="group")
            Visualization.write(bar_fig)
        else:
            Visualization.error("please select a categorical variable")
    elif plot_type == "Histogram":
        x_axis = st.sidebar.selectbox('Select X-axis', data_variables)

        bins = st.sidebar.slider("Number of Bins",0,100)

        if (data[x_axis].dtype == 'float64') or (data[x_axis].dtype == 'int64'):
            hist_fig = px.histogram(data, x=x_axis, nbins=bins)
            Visualization.write(hist_fig)
        else:
            Visualization.error("please select a numerical variable")
    elif plot_type == "Boxplot":
        x_axis = st.sidebar.selectbox('Select X-axis', data_variables)

        y_axis = st.sidebar.selectbox('Select Y-axis', data_variables)

        group = st.sidebar.selectbox('Select Group', data_variables)

        if data[x_axis].dtype == 'object':
            box_fig = px.box(data, x=x_axis, y=y_axis, color = group)
            Visualization.write(box_fig)
        else:
            Visualization.error("please select a categorical variable")
    elif plot_type == "Scatterplot":
        x_axis = st.sidebar.selectbox('Select X-axis', data_variables)

        y_axis = st.sidebar.selectbox('Select Y-axis', data_variables)

        group = st.sidebar.selectbox('Select Group', data_variables)

        if ((data[x_axis].dtype == 'float64') or (data[x_axis].dtype == 'int64')) and ((data[y_axis].dtype == 'float64') or (data[y_axis].dtype == 'int64')):
            scatter_fig = px.scatter(data, x=data[x_axis], y=data[y_axis], color=group)
            Visualization.write(scatter_fig)

        



#retun message if no file is uploaded
else:
    st.subheader("Please Upload a Valid File Format")


