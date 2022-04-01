"""
Banking Churn Prediction : Content for Pages
"""

# Authors: Tevin Temu <tevintemu@gmail.com>


import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

import os
import sys
import copy

from src.graphs import tenure, balance, est_salary

#-------------------------------------------------------------------------------
# DATA ANALYSIS
#-------------------------------------------------------------------------------

# Tenure Distribution

card_tenure = dbc.Card(
    dbc.CardBody(
        dcc.Graph(figure = tenure(), config = {"displayModeBar": False}, style = {"height": "42vh"})
    ),
    style = {"background-color": "#16103a"}
)

# balance

card_balance = dbc.Card(
    dbc.CardBody(
        dcc.Graph(figure = balance(), config = {"displayModeBar": False}, style = {"height": "42vh"})          
    ),
    style = {"background-color": "#16103a"}
)

# Total Charges Distribution

card_salary = dbc.Card(
    dbc.CardBody(
        dcc.Graph(figure = est_salary(), config = {"displayModeBar": False}, style = {"height": "42vh"})
    ),
    style = {"background-color": "#16103a"}
)

# Categorical Bar Chart

card_categorical = dbc.Card(
    dbc.CardBody(
        dbc.Spinner(
            size="md",
            color="light",
            children=[
                dcc.Graph(id="categorical_bar_graph", config = {"displayModeBar": False}, style = {"height": "48vh"})
            ]
        ),
        style = {"height": "52vh"}
    ),
    style = {"background-color": "#16103a"}
)

# Donut Chart

card_donut = dbc.Card(
    [
        dbc.CardBody(
            [
                dbc.Spinner(size="md",color="light",
                    children=[
                        dcc.Graph(id="categorical_pie_graph", config = {"displayModeBar": False}, style = {"height": "48vh"})
                    ]
                ),
                
            ], style = {"height": "52vh"}
        ),
    ],
    style = {"background-color": "#16103a"}
)

# TABS

tab_graphs = [

    # Categorical Features Visualization
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(
                        [

                            dbc.Col([
                                dbc.InputGroup(
                                    [
                                        dbc.InputGroupAddon("Categorical Feature", addon_type="prepend"),
                                        dbc.Select(
                                            options=[
                                                {"label": "Gender", "value": "Gender"},
                                                {"label": "Geography", "value": "Geography"}
                            
                                            ], id = "categorical_dropdown", value="Geography"
                                        )
                                    ]
                                ),


                                html.Img(src="../assets/customer.png", className="customer-img")
                                
                                
                                ],lg="4", sm=12,
                            ),


                            dbc.Col(card_donut, lg="4", sm=12),

                            # dbc.Spinner(id="loading2",size="md", color="light",children=[dbc.Col(card_categorical, lg="4", sm=12)]),

                            dbc.Col(card_categorical, lg="4", sm=12),

                        ], className="h-15", style={"height": "100%"}
                    )
                ]
            ),
            className="mt-3", style = {"background-color": "#272953"}
        ),

    # Tenure, Calance and TotalCharges Visualizaion

    dbc.Card(
        dbc.CardBody(
            [
                dbc.Row(
                    [
                        dbc.Col(card_tenure, lg="4", sm=12),
                        dbc.Col(card_balance, lg="4", sm=12),
                        dbc.Col(card_salary, lg="4", sm=12),  
                    ], className="h-15"
                )
            ]
        ),
        className="mt-3", style = {"background-color": "#272953"}
    )

]

tab_analysis_content = tab_graphs


# PREDICTION

tab_prediction_features = dbc.Card(
    dbc.CardBody(
        [
            # First Row

            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupAddon("Gender", addon_type="prepend"),
                                    dbc.Select(
                                        id="ft_gender",
                                        options=[
                                            {"label": "Female", "value": "Female"},
                                            {"label": "Male", "value": "Male"},
                                        ], value="Male"
                                    )
                                ]
                            )
                        ], lg="3", sm=12
                    ),

                    # Geography

                    dbc.Col(
                        [
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupAddon("Geography", addon_type="prepend"),
                                    dbc.Select(
                                        id="ft_geography",
                                        options=[
                                            {"label": "France", "value": "France"},
                                            {"label": "Spain", "value": "Spain"},
                                            {"label": "Germany", "value": "Germany"},
                                        ], value="France"
                                    )
                                ]
                            )
                        ], lg="3", sm=12
                    ),

                    # Credit Score

                    dbc.Col(
                        [
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupAddon("Credit Score", addon_type="prepend"),
                                    dbc.Input(
                                        id="ft_creditscore",
                                        placeholder="Credit Score", type="number", value="350.0"
                                    ),
                                ]
                            )
                        ], lg="3", sm=12
                    ),

                    # Age

                    dbc.Col(
                        [
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupAddon("Age", addon_type="prepend"),
                                    dbc.Input(
                                        id="ft_age",
                                        placeholder="Age", type="number", value="35"
                                    ),
                                ]
                            )
                        ], lg="3", sm=12
                    ),
                ], className="feature-row",
            ), 

            # Second Row

            dbc.Row(
                [
                    # Tenure

                    dbc.Col(
                        [
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupAddon("Tenure", addon_type="prepend"),
                                    dbc.Input(
                                        id="ft_tenure",
                                        placeholder="Tenure", type="number", value="5"
                                    ),
                                ]
                            )
                        ], lg="3", sm=12
                    ),

                    # Balance

                    dbc.Col(
                        [
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupAddon("Balance", addon_type="prepend"),
                                    dbc.Input(
                                        id="ft_balance",
                                        placeholder="Balance", type="number", value="75000.0"
                                    ),
                                ]
                            )
                        ], lg="3", sm=12
                    ),

                    # NumOfProducts

                     dbc.Col(
                        [
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupAddon("NumOfProducts", addon_type="prepend"),
                                    dbc.Input(
                                        id="ft_numofproducts",
                                        placeholder="NumOfProducts", type="number", value="2"
                                    ),
                                ]
                            )
                        ], lg="3", sm=12
                    ),

                    # HasCrCard

                    dbc.Col(
                        [
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupAddon("HasCrCard", addon_type="prepend"),
                                    dbc.Select(
                                        id="ft_hascrcard",
                                        options=[
                                            {"label": "Yes", "value":"1"},
                                            {"label": "No", "value":"0"},
                                        ], value="0"
                                    )
                                ]
                            )
                        ], lg="3", sm=12
                    )
                ], className="feature-row",
            ),

            # Third Row

            dbc.Row(
                [
                    # IsActiveMember

                    dbc.Col(
                        [
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupAddon("IsActiveMember", addon_type="prepend"),
                                    dbc.Select(
                                        id="ft_isactivemember",
                                        options=[
                                            {"label": "Yes", "value":"1"},
                                            {"label": "No", "value": "0"},
                                        ], value="0"
                                    )
                                ]
                            )
                        ], lg="3", sm=12
                    ),

                    # Estimated Salary

                    dbc.Col(
                        [
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupAddon("EstimatedSalary", addon_type="prepend"),
                                    dbc.Input(
                                        id="ft_estimatedsalary",
                                        placeholder="Estimated Salary", type="number", value="75000.0"
                                    ),
                                ]
                            )
                        ], lg="3", sm=12
                    ),

                    #Age Bins
                    dbc.Col(
                        [
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupAddon("AgeBin", addon_type="prepend"),
                                    dbc.Select(
                                        id="ft_agebin",
                                        options=[
                                            {"label": "Young", "value":"Young"},
                                            {"label": "Adult", "value": "Adult"},
                                            {"label": "Old", "value": "Old"},
                                        ], value="Young"
                                    )
                                ]
                            )
                        ], lg="3", sm=12
                    ),

                ], className="feature-row",
            ),

        ]
    ),
    className="mt-3", style = {"background-color": "#272953"}
)

tab_prediction_result = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Button("Predict", id='btn_predict', size="lg", className="btn-predict")
                        ], lg="4", sm=4, style={"display": "flex", "align-items":"center", "justify-content":"center"},
                        className="card-padding"
                    ),

                    dbc.Col(
                        [
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        dbc.Spinner(html.H4(id="lgbc_result", children="-", style={'color':'#e7b328'}), size="sm", spinner_style={'margin-bottom': '5px'}),
                                        html.P("LightGBMClassifier")
                                    ]
                                ), className="result-card", style={"height":"16vh"}
                            )
                        ], lg=4, sm=4, className="card-padding"
                    ),

                    dbc.Col(
                        [
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        dbc.Spinner(html.H4(id="rf_result", children="-", style={'color':'#e7b328'}), size="sm", spinner_style={'margin-bottom': '5px'}),
                                        html.P("RandomForestClassifier")
                                    ]
                                ), className="result-card", style={"height":"16vh"}
                            )
                        ], lg=4, sm=4, className="card-padding"
                    )


                ]
            ),


        ]
    ),
    className="mt-3", style = {"background-color": "#272953"}
)

tab_prediction_content = [
    
    tab_prediction_features,
    tab_prediction_result
    
]