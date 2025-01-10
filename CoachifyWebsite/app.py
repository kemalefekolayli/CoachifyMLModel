import dash
from dash import dcc, html, dash_table, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from monthly_spending_page import monthly_spending_page, register_callbacks
from youtube_analytics import youtube_analytics_page



# Load data
mentor_efficiency_data = pd.read_csv("CoachifyWebsite/data/mentor_summary.csv")
mentor_payment_dropout_data = pd.read_csv("CoachifyWebsite/data/mentor_payment_dropout_analysis.csv")



# Initialize Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = "Coachify Dashboard"

# Navbar
def create_navbar():
    return dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("Mentor Efficiency", href="/mentor-efficiency")),
            dbc.NavItem(dbc.NavLink("Dropout Analysis", href="/dropout-analysis")),
            dbc.NavItem(dbc.NavLink("Compare Mentors", href="/compare-mentors")),
            dbc.NavItem(dbc.NavLink("Monthly Spending Page", href="/monthly_spending")),
            dbc.NavItem(dbc.NavLink("Youtube Analytics", href="/youtube_analytics"))
        ],
        brand="Coachify Dashboard",
        brand_href="/",
        color="primary",
        dark=True
    )

# Welcome Page
# Updated Home Page Layout
# Updated Home Page Layout
welcome_page = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Welcome to Coachify Dashboard", className="text-center mt-5"), width=12)
    ]),
    dbc.Row([
        dbc.Col(html.H3("Kemal Efe Kolaylı - Student ID: 32372", className="text-center mb-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col(html.P("""
            This dashboard provides a comprehensive analysis of various data points for Coachify, a platform for student mentoring.Due to all of the data being hand written by
            a college student working on a start-up for the first time, there are some missing values and inconsistencies in the data. The data has been cleaned and processed to provide meaningful insights.
            Below is an overview of the analyses conducted:
        """, className="text-center mb-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col(html.Ul([
            html.Li("Mentor Efficiency Analysis: Compare mentor performance based on payments, retention rates, and cost efficiency."),
            html.Li("Dropout Analysis: Understand the dropout rates of students across different mentors."),
            html.Li("Monthly Spending and Growth: Analyze monthly spending across categories and correlate it with student gains."),
            html.Li("YouTube Analytics: Visualize monthly YouTube viewership data and its correlation with student growth."),
            html.Li("Mentor Comparison: Directly compare two mentors on key performance metrics."),
        ], className="text-left"), width={"size": 8, "offset": 2})
    ]),
    dbc.Row([
        dbc.Col(html.Div([
            html.P("Visit us online:", className="text-center mt-4"),
            html.A("Coachify Website", href="https://coachifyedu.com/", target="_blank", className="d-block text-center"),
            html.A("@coachifyedu on Instagram", href="https://www.instagram.com/coachifyedu/", target="_blank", className="d-block text-center")
        ]), width={"size": 6, "offset": 3})
    ]),
    
])

# Mentor Efficiency Page
mentor_efficiency_page = dbc.Container([
    dbc.Row([dbc.Col(html.H1("Mentor Efficiency Dashboard", className="text-center mt-5"), width=12)]),
    dbc.Row([
        dbc.Col(dcc.Graph(
            id="efficiency-scatter",
            figure=px.scatter(
                mentor_efficiency_data,
                x="Total Payment",
                y="Cost Efficiency",
                color="Student Count",
                size="Average Retention",
                hover_name="Mentor",
                title="Mentor Payments vs Cost Efficiency"
            )
        ), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.Label("Search for a Mentor:"),
            dcc.Input(id="mentor-search", type="text", placeholder="Enter mentor name", className="form-control mb-3")
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col(
            dash_table.DataTable(
                id="mentor-efficiency-table",
                columns=[
                    {"name": i, "id": i} for i in mentor_efficiency_data.columns if i != "Composite"
                ],
                data=mentor_efficiency_data.to_dict("records"),
                style_table={"overflowX": "auto"},
                style_cell={"textAlign": "left"}
            ),
            width=12
        )
    ]),
    dbc.Row([
        dbc.Col(dbc.Button("Compare Mentors", href="/compare-mentors", color="info", className="mt-4"), width=6),
        dbc.Col(dbc.Button("Back to Home", href="/", color="primary", className="mt-4"), width=6)
    ])
])

# Compare Mentors Page
compare_mentors_page = dbc.Container([
    dbc.Row([dbc.Col(html.H1("Compare Mentors", className="text-center mt-5"), width=12)]),
    dbc.Row([
        dbc.Col([
            html.Label("Select Mentor 1:"),
            dcc.Dropdown(
                id="mentor-1-dropdown",
                options=[{"label": name, "value": name} for name in mentor_efficiency_data["Mentor"].unique()],
                placeholder="Select Mentor 1"
            )
        ], width=6),
        dbc.Col([
            html.Label("Select Mentor 2:"),
            dcc.Dropdown(
                id="mentor-2-dropdown",
                options=[{"label": name, "value": name} for name in mentor_efficiency_data["Mentor"].unique()],
                placeholder="Select Mentor 2"
            )
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col(html.Div(id="comparison-output"), width=12)
    ]),
    dbc.Row([dbc.Col(dbc.Button("Back to Mentor Efficiency", href="/mentor-efficiency", color="secondary", className="mt-4"), width=6)])
])
# Dropout Analysis Page
dropout_analysis_page = dbc.Container([
    dbc.Row([dbc.Col(html.H1("Dropout Rate Analysis", className="text-center mt-5"), width=12)]),

    # Updated Graph
    dbc.Row([dbc.Col(dcc.Graph(
        id="dropout-rate-bar",
        figure=px.bar(
            mentor_payment_dropout_data.sort_values(by="Dropout Rate", ascending=False),
            x="Dropout Rate",
            y="Mentor",
            orientation="h",
            title="Dropout Rate by Mentor",
            color="Dropout Rate",
            color_continuous_scale="Blues",
            labels={"Dropout Rate": "Dropout Rate (%)", "Mentor": "Mentor Name"}
        ).update_layout(
            xaxis=dict(range=[0, 1], title="Dropout Rate (%)"),
            yaxis=dict(title="Mentor Name", automargin=True),
            margin=dict(l=10, r=10, t=30, b=10),
            height=800,
            bargap=0.1
        )
    ), width=12)]),

    # Table Below Graph
    dbc.Row([dbc.Col(html.H3("Detailed Dropout Data", className="text-center mt-4"), width=12)]),
    dbc.Row([dbc.Col(
        dash_table.DataTable(
            id="dropout-analysis-table",
            columns=[{"name": i, "id": i} for i in mentor_payment_dropout_data.columns],
            data=mentor_payment_dropout_data.to_dict("records"),
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left", "padding": "10px"},
            style_header={"backgroundColor": "lightblue", "fontWeight": "bold"},
            style_data={"border": "1px solid gray"}
        ), width=12
    )]),

    # Back to Home Button
    dbc.Row([dbc.Col(dbc.Button("Back to Home", href="/", color="primary", className="mt-4"), width=12)])
])

# App Layout
app.layout = dbc.Container([
    create_navbar(),
    dcc.Location(id="url"),
    html.Div(id="page-content")
], fluid=True)

# Callbacks
@app.callback(
    Output("mentor-efficiency-table", "data"),
    Input("mentor-search", "value")
)
def update_table(search_value):
    if not search_value:
        return mentor_efficiency_data.to_dict("records")
    filtered_data = mentor_efficiency_data[mentor_efficiency_data["Mentor"].str.contains(search_value, case=False, na=False)]
    return filtered_data.to_dict("records")

@app.callback(
    Output("comparison-output", "children"),
    [Input("mentor-1-dropdown", "value"), Input("mentor-2-dropdown", "value")]
)
def compare_mentors(mentor1, mentor2):
    if not mentor1 or not mentor2:
        return html.P("Please select two mentors to compare.")

    mentor1_data = mentor_efficiency_data[mentor_efficiency_data["Mentor"] == mentor1].iloc[0]
    mentor2_data = mentor_efficiency_data[mentor_efficiency_data["Mentor"] == mentor2].iloc[0]

    comparison_table = dbc.Table([
        html.Thead(html.Tr([html.Th("Metric"), html.Th(mentor1), html.Th(mentor2)])),
        html.Tbody([
            html.Tr([html.Td("Student Count"), html.Td(mentor1_data["Student Count"]), html.Td(mentor2_data["Student Count"])]),
            html.Tr([html.Td("Average Retention"), html.Td(mentor1_data["Average Retention"]), html.Td(mentor2_data["Average Retention"])]),
            html.Tr([html.Td("Total Payment"), html.Td(mentor1_data["Total Payment"]), html.Td(mentor2_data["Total Payment"])]),
            html.Tr([html.Td("Cost Efficiency"), html.Td(mentor1_data["Cost Efficiency"]), html.Td(mentor2_data["Cost Efficiency"])]),
        ])
    ], bordered=True, hover=True, striped=True)

    return comparison_table

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/mentor-efficiency":
        return mentor_efficiency_page
    elif pathname == "/dropout-analysis":
        return dropout_analysis_page
    elif pathname == "/compare-mentors":
        return compare_mentors_page
    elif pathname == "/monthly_spending":
        return monthly_spending_page
    elif pathname == "/youtube_analytics":
        return youtube_analytics_page
    else:
        return welcome_page
    

if __name__ == "__main__":
    register_callbacks(app)
    app.run_server(debug=True)