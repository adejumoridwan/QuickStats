#----------------------------------------------------------------------------------------------------------------------------
#importing required libraries
#----------------------------------------------------------------------------------------------------------------------------
#streamlit
import streamlit as st
#numpy
import numpy as np
#pandas
import pandas as pd
#plotly
import plotly.express as px
#scipy
import scipy.stats as stats
from scipy.stats import pearsonr
from scipy.stats import f_oneway
from scipy.stats import chisquare
from scipy.stats import chi2_contingency
#statsmodels
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.graphics.api import interaction_plot, abline_plot
from statsmodels.stats.anova import anova_lm

#----------------------------------------------------------------------------------------------------------------------------
#Function running the web app
#----------------------------------------------------------------------------------------------------------------------------
def analysis(data):
    #Tabs on the app
    Data, Descriptive, Visualization, Statistics = st.tabs(["Data", "Descriptive","Visualization","Statistics"])
    
    #Display data on data tab
    Data.dataframe(data)

    #Display descriptive statistics on Descriptive tab
    Descriptive.header("Descriptive Statistics")
    Descriptive.table(data.describe())

    #Visualization tabs
    data_variables = data.columns

    #Sidebar Visualization controls
    st.sidebar.header("Visualization Controls")
    plot_type = st.sidebar.selectbox("Select Plot Type", ("BarChart","Histogram","Boxplot","Scatterplot","Lineplot"))

    #----------------------------------------------------------------------------------------------------------------------------
    #Condition plotting various visualizations
    #----------------------------------------------------------------------------------------------------------------------------
    #Plot barchart if barchart is selected
    if plot_type == "BarChart":
        x_axis = st.sidebar.selectbox('Select X-axis', data_variables)
        group = st.sidebar.selectbox('Select Group', data_variables)

        if data[x_axis].dtype == 'object': #Plot bar plot if variable is not numeric
            bar_fig = px.bar(data, x=x_axis, color = group, barmode="group")
            Visualization.write(bar_fig)
        else:
            Visualization.error("please select a categorical variable")

    #Plot histogram if histogram option is selected
    elif plot_type == "Histogram":
        x_axis = st.sidebar.selectbox('Select X-axis', data_variables)
        bins = st.sidebar.slider("Number of Bins",0,100)

        if (data[x_axis].dtype == 'float64') or (data[x_axis].dtype == 'int64'): #Plot histogam if variable is numeric
            hist_fig = px.histogram(data, x=x_axis, nbins=bins)
            Visualization.write(hist_fig)
        else:
            Visualization.error("please select a numerical variable")

    #Plot boxplot if histogram option is selected
    elif plot_type == "Boxplot":
        x_axis = st.sidebar.selectbox('Select X-axis', data_variables)
        y_axis = st.sidebar.selectbox('Select Y-axis', data_variables)
        group = st.sidebar.selectbox('Select Group', data_variables)

        if data[x_axis].dtype == 'object': #Plot boxplot if non-numeric variable is selected
            box_fig = px.box(data, x=x_axis, y=y_axis, color = group)
            Visualization.write(box_fig)
        else:
            Visualization.error("please select a categorical variable")

    #Plot scatterplot when scatterplot option is selected
    elif plot_type == "Scatterplot":
        x_axis = st.sidebar.selectbox('Select X-axis', data_variables)
        y_axis = st.sidebar.selectbox('Select Y-axis', data_variables)
        group = st.sidebar.selectbox('Select Group', data_variables)

        #plot scatterplot only when numeric variable is selected
        if ((data[x_axis].dtype == 'float64') or (data[x_axis].dtype == 'int64')) and ((data[y_axis].dtype == 'float64') or (data[y_axis].dtype == 'int64')):
            scatter_fig = px.scatter(data, x=x_axis, y=y_axis, color=group)
            Visualization.write(scatter_fig)
        else:
            Visualization.error("please select a numeric variable")

    #Plot lineplot when lineplot is selected        
    else:
        x_axis = st.sidebar.selectbox('Select X-axis', data_variables)
        y_axis = st.sidebar.selectbox('Select Y-axis', data_variables)
        group = st.sidebar.selectbox('Select Group', data_variables)

        lineplot = px.line(data, x=x_axis, y=y_axis)
        Visualization.write(lineplot)

    #----------------------------------------------------------------------------------------------------------------------------
    #Statistical Analysis
    #----------------------------------------------------------------------------------------------------------------------------
    st.sidebar.header("Statisitical Analysis")
    select_stat = st.sidebar.selectbox("Select a Statistical Analysis", ["Correlation", "Linear Regression","t-test","One Way", "Two-Way ANOVA","Chi-Square",])

    #Perfrom Correlation Analyssi if correlation is selected


use_default = st.checkbox("Use Default Dataset")
st.sidebar.header("Upload Data")

#Upload File
uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel File", type=["csv", "xlsx"])


#----------------------------------------------------------------------------------------------------------------------------
#What to display when file is uploaded or not uploaded
#----------------------------------------------------------------------------------------------------------------------------
if use_default:
    if uploaded_file is None:
        data = pd.read_csv("sales.csv")
        analysis(data)
else:
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        analysis(data)

