"""
Customer Churn
"""

# Authors: Tevin Temu <tevintemu@gmail.com>

import dash
import dash_bootstrap_components as dbc
from  dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
from dash import no_update

import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

import os
import sys
import copy
import time

from src.navbar import get_navbar   # navbar function
from src.graphs import df, lgb_model, rf_model,layout 
from content import tab_prediction_content, tab_analysis_content

# Creating the app

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    external_stylesheets = [dbc.themes.SUPERHERO,'/assets/styles.css']
) 

server=app.server

# Tabs Content

tabs = dbc.Tabs(
    [
        dbc.Tab(tab_prediction_content, label="Prediction"),
        dbc.Tab(tab_analysis_content, label="Data Analysis"),
    ]
)

# Jumbotron

jumbotron = dbc.Jumbotron(
    html.H4("Banking Churn Analysis and Prediction."),
    className="cover"
)

#-------------------------------------------------------------------------------
# APPLICATION LAYOUT
#-------------------------------------------------------------------------------

app.layout = html.Div(
    [
        get_navbar(),
        jumbotron,
        html.Div(
            dbc.Row(dbc.Col(tabs, width=12)),
            id="mainContainer",
            style={"display": "flex", "flex-direction": "column"}
        ),
        html.P("Developed by Tevin Temu.", className="footer")
    ],
)

#-------------------------------------------------------------------------------
# CALLBACKS
#-------------------------------------------------------------------------------

# Data Analysis Tab - Categorical Bar Chart 

#@app.callback(
 #   Output("categorical_bar_graph", "figure"),
  #  [
   #     Input("categorical_dropdown", "value"),
    #],
#)

def bar_categorical(feature):

    time.sleep(0.2)
# nnededs to be fixed
   # temp = df.groupby([feature, 'Exited']).count()['CustomerId'].reset_index().dropna(inplace=True)
    temp = df.groupby([feature])['Exited']
    fig = px.bar(temp,x=feature, y="Exited",
             #color=temp['Exited'].map({'1': 'Churn', '0': 'NoChurn'}),
             color_discrete_map={"Exited": "#47acb1", "NoChurn": "#f26522"},
             barmode='group')
    
    layout_count = copy.deepcopy(layout)
    fig.update_layout(layout_count)
    
    _title = (feature[0].upper() + feature[1:]) + " Distribution by Churn"
    
    fig.update_layout(
        title = {'text': _title, 'x': 0.5},
        #xaxis_visible=False,
        xaxis_title="",
        yaxis_title="Count",
        legend_title_text="",
        legend = {'x': 0.16}
    )
    return fig

@app.callback(
    Output("categorical_pie_graph", "figure"),
    [
        Input("categorical_dropdown", "value"),
    ],
)

# Data Analysis Tab - Donut Chart 

def donut_categorical(feature):

    time.sleep(0.2)

    temp = df.groupby([feature]).count()['CustomerId'].reset_index()

    fig = px.pie(temp, values="CustomerId", names=feature, hole=.5)

    layout_count = copy.deepcopy(layout)
    fig.update_layout(layout_count)
    
    _title = (feature[0].upper() + feature[1:]) + " Percentage"

    if(df[feature].nunique() == 2):
        _x = 0.3
    elif(df[feature].nunique() == 3):
        _x = 0.16
    else:
        _x = 0

    fig.update_layout(
        title = {'text': _title, 'x': 0.5},
        legend = {'x': _x}
    )

    return fig

# Prediction Tab - Predict and Update the Result Cards 

@app.callback(
    [dash.dependencies.Output('lgbc_result', 'children'),
     dash.dependencies.Output('rf_result', 'children')],

    [dash.dependencies.Input('btn_predict', 'n_clicks')],

    [dash.dependencies.State('ft_gender', 'value'),
     dash.dependencies.State('ft_geography', 'value'),
     dash.dependencies.State('ft_creditscore', 'value'),
     dash.dependencies.State('ft_age', 'value'),
     dash.dependencies.State('ft_tenure', 'value'),
     dash.dependencies.State('ft_balance', 'value'),
     dash.dependencies.State('ft_numofproducts', 'value'),
     dash.dependencies.State('ft_hascrcard', 'value'),
     dash.dependencies.State('ft_isactivemember', 'value'),
     dash.dependencies.State('ft_estimatedsalary', 'value'),
     dash.dependencies.State('ft_agebin', 'value'),
     ]
)

def predict_churn(n_clicks, ft_gender, ft_geography, ft_creditscore, ft_age, ft_tenure,
                            ft_balance, ft_numofproducts, ft_hascrcard, ft_isactivemember,
                            ft_estimatedsalary,ft_agebin):

    time.sleep(0.4)

    sample = {'Gender': ft_gender, 'Geography': ft_geography, 'CreditScore': float(ft_creditscore),
              'Age': int(ft_age), 'Tenure': int(ft_tenure),
              'Balance': float(ft_balance), 'NumofProducts': int(ft_numofproducts), 'HasCrCard':int(ft_hascrcard),
              'IsActiveMember': int(ft_isactivemember), 'EstimatedSalary': float(ft_estimatedsalary),'Age_bins': ft_agebin}

    sample_df = pd.DataFrame(sample, index=[0])
    sample_df['Geography'] =pd.factorize(sample_df['Geography'])[0]
    sample_df['Gender'] =pd.factorize(sample_df['Gender'])[0]
    sample_df['Age_bins']=pd.factorize(sample_df['Age_bins'])[0]
    #sample_df_enc = pd.DataFrame(sample_df_enc)

    #sample_df_enc = pd.concat([sample_df_enc, sample_df[['CreditScore', 'Age', 'Tenure', 'Balance','NumofProducts','HasCrCard','IsActiveMember','EstimatedSalary','Age_bins']]], axis=1)

    lgb_prediction = lgb_model.predict(sample_df)
    rf_prediction = rf_model.predict(sample_df)

    def churn_to_text(num):
        if(num == 0):
            return "Predicted: Not Churn"
        elif(num == 1):
            return "Predicted: Churn"

    # print(svm_prediction)

    if(n_clicks):
        return churn_to_text(lgb_prediction), churn_to_text(rf_prediction)
    else:
        return no_update

@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)

# Navbar Toggle Callback for Mobile Devices

def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

#-------------------------------------------------------------------------------
# MAIN FUNCTION
#-------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run_server(debug=True, port=8050)