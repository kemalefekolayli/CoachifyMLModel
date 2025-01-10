import pandas as pd
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Load data
roi_data = pd.read_csv("CoachifyWebsite/data/monthly_roi_summary.csv")

# Reshape the data for category spending
melted_roi_data = roi_data.melt(
    id_vars=["Month", "Student Gain", "Total Spending", "Total ROI"],
    var_name="Category",
    value_name="Amount Spent"
)

# Monthly Spending Page Layout
monthly_spending_page = dbc.Container([
    dbc.Row([dbc.Col(html.H1("Monthly Spending and ROI Analysis", className="text-center mt-5"), width=12)]),

    # Dropdown for selecting a single month
    dbc.Row([
        dbc.Col([
            html.Label("Select a Month:"),
            dcc.Dropdown(
                id="single-month-dropdown",
                options=[{"label": month, "value": month} for month in roi_data["Month"].unique()],
                placeholder="Select a month"
            )
        ], width=6),
    ]),

    # Pie charts for spending breakdown
    dbc.Row([
        dbc.Col(dcc.Graph(id="spending-breakdown-pie"), width=6),
        dbc.Col(dcc.Graph(id="student-gain-roi-pie"), width=6),
    ]),

    # Dropdown for comparing months
    dbc.Row([
        dbc.Col([
            html.Label("Compare Months:"),
            dcc.Dropdown(
                id="compare-months-dropdown",
                options=[{"label": month, "value": month} for month in roi_data["Month"].unique()],
                placeholder="Select months to compare",
                multi=True
            )
        ], width=12)
    ]),

    # Comparison Graphs
    dbc.Row([
        dbc.Col(dcc.Graph(id="roi-comparison-graph"), width=6),
        dbc.Col(dcc.Graph(id="student-gain-comparison-graph"), width=6)
    ]),

    dbc.Row([dbc.Col(dbc.Button("Back to Home", href="/", color="primary", className="mt-4"), width=12)])
])

# Callbacks for the Monthly Spending Page
def register_callbacks(app):
    # Callback for spending breakdown pie chart
    @app.callback(
        [Output("spending-breakdown-pie", "figure"),
         Output("student-gain-roi-pie", "figure")],
        Input("single-month-dropdown", "value")
    )
    def update_pie_charts(selected_month):
        if not selected_month:
            return px.pie(title="Select a month to view spending breakdown"), px.pie(title="Select a month to view ROI")

        filtered_data = melted_roi_data[melted_roi_data["Month"] == selected_month]
        if filtered_data.empty:
            return px.pie(title="No data available for the selected month"), px.pie(title="No data available for the selected month")

        spending_pie = px.pie(
            filtered_data,
            names="Category",
            values="Amount Spent",
            title=f"Spending Breakdown for {selected_month}"
        )

        roi_pie = px.pie(
            filtered_data,
            names="Category",
            values="Amount Spent",  # Replace this with ROI calculation if needed
            title=f"ROI Contribution for {selected_month}"
        )

        return spending_pie, roi_pie

    # Callback for ROI and Student Gain Comparison
    @app.callback(
        [Output("roi-comparison-graph", "figure"),
         Output("student-gain-comparison-graph", "figure")],
        Input("compare-months-dropdown", "value")
    )
    def update_comparison_graphs(selected_months):
        if not selected_months or len(selected_months) < 2:
            return px.bar(title="Select at least two months to compare ROI"), px.bar(title="Select at least two months to compare Student Gains")

        filtered_data = roi_data[roi_data["Month"].isin(selected_months)]

        roi_comparison = px.bar(
            filtered_data,
            x="Month",
            y="Total ROI",
            title="ROI Comparison Across Months",
            labels={"Total ROI": "Return on Investment"}
        )

        student_gain_comparison = px.bar(
            filtered_data,
            x="Month",
            y="Student Gain",
            title="Student Gain Comparison Across Months",
            labels={"Student Gain": "Number of Students"}
        )

        return roi_comparison, student_gain_comparison
