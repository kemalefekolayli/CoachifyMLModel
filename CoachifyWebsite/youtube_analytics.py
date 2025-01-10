import pandas as pd
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Load combined data
combined_data = pd.read_csv("combined_data.csv")

# Load correlation result
with open("correlation_result.txt", "r") as f:
    correlation_result = f.read()

# YouTube Analytics Page Layout
youtube_analytics_page = dbc.Container([
    dbc.Row([dbc.Col(html.H1("YouTube Analytics", className="text-center mt-5"), width=12)]),

    # YouTube Views Graph
    dbc.Row([dbc.Col(dcc.Graph(
        id="youtube-views-graph",
        figure=px.bar(
            combined_data,
            x="Month",
            y="Monthly YouTube Views",
            title="Monthly YouTube Views",
            labels={"Month": "Month", "Monthly YouTube Views": "Views"}
        )
    ), width=12)]),

    # Display Correlation Result
    dbc.Row([
        dbc.Col(html.Div([
            html.H3("Correlation Analysis", className="text-center mt-4"),
            html.P(correlation_result, className="text-center")
        ]), width=12)
    ]),

    # Back to Home Button
    dbc.Row([dbc.Col(dbc.Button("Back to Home", href="/", color="primary", className="mt-4"), width=12)])
])

# Register Callback (Optional for interaction, none needed here)
def register_callbacks(app):
    pass
