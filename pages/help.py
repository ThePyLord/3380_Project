import dash
from dash import dcc, html, callback, Output, Input, dash_table, State


dash.register_page(__name__, path="/help")

layout = html.Div(
    [
        html.H1("Help"),
        html.P(
            "This is a simple web application that allows you to explore Formula 1 data."
        ),
        html.H2("How to use"),
        html.P(
            "Use the navigation bar at the side of the page to navigate between pages."
        ),
        html.P(
            "In queries with dropdowns, select the desired option from the dropdown."
        ),
        html.P("You can also search by typing to filter the dropdown options."),
        html.P(
            "For queries with more than one dropdown, select an option from each dropdown in order from left to right."
        ),
        html.P("Click the 'Submit' button to run the query."),
        html.P(
            "If any of the dropdowns in the query are empty, it means there is no data available for that query."
        ),
		html.H2("Plots"),
		html.P("The plots in this web application are interactive. You can hover over data points to see more information."),
		html.P("You can also zoom in and out of the plots by clicking and dragging."),
		html.P("Click on items in the legend to hide or show data points."),
        html.H2("About the data"),
        dcc.Markdown(
            """The data used in this web application is from the [Kaggle Formula 1 World Championship](https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020?rvi=1) dataset, which provides data on the Formula One World Championship"""
        ),
    ]
)
