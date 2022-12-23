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
from scipy.stats import chi2_contingency 

#statsmodels
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.graphics.api import interaction_plot, abline_plot
from statsmodels.stats.anova import anova_lm


def main():
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
        st.sidebar.header("Statistical Analysis")
        select_stat = st.sidebar.selectbox("Select a Statistical Analysis", ["Correlation", "Linear Regression","t-test","ANOVA(One-Way)", "ANOVA(Two-Way)","Chi-Square",])
        col1, col2= Statistics.columns([1, 5])

        #Perfrom Correlation Analysis if correlation is selected
        if select_stat == "Correlation":
            with col1:
                cor_var1 = st.selectbox("Variable 1", data_variables)
                cor_var2 = st.selectbox("Variable 2", data_variables)
            
            with col2:
                    if (data[cor_var1].dtype in ["float64","int64"]) and (data[cor_var2].dtype in ["float64","int64"]):
                        corr = pearsonr(data[cor_var1], data[cor_var2])
                        st.subheader(f"The correlation coefficient(r) between {cor_var1} and {cor_var2} is {round(corr[0],4)}")
                    else:
                        st.error("Please select numeric variables")
        
        #Perfrom regression Analysis if regression is selected
        elif select_stat == "Linear Regression":
            with col1:
                output = st.selectbox("Response Variable", data_variables)
                predictor = st.multiselect("Predictor Variables", data_variables)
            with col2:
                if (data[output].dtype in ["float64","int64"]) or (data[predictor].dtype in ["float64","int64"]):
                    formula = "data[output] ~ data[predictor]"
                    lm = ols(formula, data).fit()
                    st.write(lm.summary())
                else:
                    col2.error("Please select numeric variables")

        #perform t-test analysis
        elif select_stat == "t-test":
            with col1:
                cat_var = st.selectbox("Categorial Variable",data_variables)
                cont_var = st.selectbox("Continous Variable", data_variables)
                groups = data[cat_var].unique()
                group_1 = st.selectbox("Group 1", groups)
                group_2 = st.selectbox("Group 2", groups)
            
            with col2:
                if data[cat_var].dtype not in ["float64", "int64"] and data[cont_var].dtype in ["float64", "int64"]:
                        x = data.loc[data[cat_var] == group_1, cont_var]
                        y = data.loc[data[cat_var] == group_2, cont_var]
                        t_test = stats.ttest_ind(x, y)
                        if t_test[1] < 0.05:
                            st.write(f"Reject Null Hypothesis since p-value < 0.05 and t-test statistic = {round(t_test[0],4)}")
                        else:
                            st.write(f"Fail to reject Null Hypothesis since p-value > 0.05 and t-test statistic = {round(t_test[0],4)}")
                else:
                    st.error("Please the specify the right variables")


        #perform two-way anova test
        elif select_stat == "ANOVA(Two-Way)":
            with col1:
                resp = st.selectbox("Response Variable", data_variables)
                factor_A = st.selectbox("Factor A", data_variables)
                factor_B = st.selectbox("Factor B", data_variables)

            with col2:
                if (data[resp].dtype in ["float64","int64"]) and (data[factor_A].dtype == "object") and (data[factor_B].dtype == "object"):
                    response = data[resp]
                    A = data[factor_A]
                    B = data[factor_B]
                    formula = "response ~ A + B + A:B"
                    lm = ols(formula, data=data).fit()
                    anova_table = sm.stats.anova_lm(lm, typ = 2)
                    st.write(anova_table)
                else:
                    st.error("please give the right variables")

        #Perform chi-square analysis
        elif select_stat == "Chi-Square":
            with col1:
                chisq_var_A = st.selectbox("Factor A", data_variables)
                chisq_var_B = st.selectbox("Factor B", data_variables)

            with col2:
                if data[chisq_var_A].dtype == "object" and data[chisq_var_B].dtype == "object":
                    cross_tab = pd.crosstab(index=data[chisq_var_A], columns=data[chisq_var_B])
                    st.table(cross_tab)
                    cross_tab_matrix = np.array(cross_tab)
                    chisq_analysis = chi2_contingency(cross_tab_matrix)
                    if chisq_analysis[1] < 0.05:
                        st.write(f"Dependent(Reject Null Hypothesis)")
                    else:
                        st.write(f"Independent(Fail to reject Null Hypothesis)")

                else:
                    st.error("please give the right variables")

        elif select_stat == "ANOVA(One-Way)":
            with col1:
                resp = st.selectbox("Response", data_variables)
                factor = st.selectbox("Factor", data_variables)
            with col2:
                if (data[resp].dtype in ["float64","int64"]) and (data[factor].dtype == "object"):
                    response = data[resp]
                    Factor = data[factor]                
                    formula = "response ~ Factor"
                    lm = ols(formula, data=data).fit()
                    anova_table = sm.stats.anova_lm(lm, typ = 1)
                    st.write(anova_table)
                else:
                    st.error("please give the right variables")
                


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


if __name__ == "__main__":
    main()
