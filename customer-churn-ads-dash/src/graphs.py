import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
#import dash_core_components as dcc
from dash import dcc
from dash.dependencies import Input, Output, State

import pandas as pd
import joblib
import plotly.express as px
import plotly.figure_factory as ff
from pathlib import Path
import copy

layout = dict(
    autosize=True,
    #automargin=True,
    margin=dict(l=20, r=20, b=20, t=30),
    hovermode="closest",
    plot_bgcolor="#16103a",
    paper_bgcolor="#16103a",
    legend=dict(font=dict(size=10), orientation="h"),
    title="Satellite Overview",
    font_color ="#e0e1e6",
    xaxis_showgrid=False,
    yaxis_showgrid=False
)

# Model Read
lgb_path = 'data/lgbm_model.sav'
lgb_model = joblib.load(lgb_path)

rf_path = 'data/classifierrandom_model.sav'
rf_model = joblib.load(rf_path)

# Data Read
#file= Path(r'C:\Users\DELL\OneDrive\Desktop\ADS Assignment\customer-churn\data\banking_churn.csv')
df = pd.read_csv('data/banking_churn.csv')
df['Age_bins'] = pd.cut(df['Age'], bins=3, labels=['Young', 'Adult', 'Elderly'])
feature= df[['Geography','Gender']]

# Encoding categorical features
#from sklearn.preprocessing import OneHotEncoder
#ohe = OneHotEncoder(sparse=False)
#ohe.fit(df[cat_features])


def tenure():
    x1 = df[df['Exited'] == 0]['Tenure']
    x2 = df[df['Exited'] == 1]['Tenure']
    
    
    
    fig = ff.create_distplot([x1,x2], group_labels= ['No', 'Yes'],
                             bin_size=3,
                             curve_type='kde',
                             show_rug=False,
                             show_hist=False,
                             show_curve=True,
                             colors=['#47acb1','#f26522'])
    
    layout_count = copy.deepcopy(layout)
    fig.update_layout(layout_count)
    
    fig.update_layout(
        title = {'text': 'KDE of Tenures', 'x': 0.5},
        legend = {'x': 0.25}
    )
    
    return fig


def balance():
    x1 = df[df['Exited'] == 0]['Balance']
    x2 = df[df['Exited'] == 1]['Balance']
    
    
    
    fig = ff.create_distplot([x1,x2], group_labels= ['No', 'Yes'],
                             bin_size=3,
                             curve_type='kde',
                             show_rug=False,
                             show_hist=False,
                             show_curve=True,
                             colors=['#47acb1','#f26522'])
    
    layout_count = copy.deepcopy(layout)
    fig.update_layout(layout_count)
    
    fig.update_layout(
        title = {'text': 'KDE of Balance', 'x': 0.5},
        legend = {'x': 0.25}
        
    )
    
    return fig


def est_salary():
    x1 = df[df['Exited'] == 0]['EstimatedSalary']
    x2 = df[df['Exited'] == 1]['EstimatedSalary']
    
    
    
    fig = ff.create_distplot([x1,x2], group_labels= ['No', 'Yes'],
                             bin_size=3,
                             curve_type='kde',
                             show_rug=False,
                             show_hist=False,
                             show_curve=True,
                             colors=['#47acb1','#f26522'])
    
    layout_count = copy.deepcopy(layout)
    fig.update_layout(layout_count)
    
    fig.update_layout(
        title = {'text': 'KDE of Estimated Salary', 'x': 0.5},
        legend = {'x': 0.25}
    )
    
    return fig



