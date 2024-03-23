import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from queries import Queries


dash.register_page(__name__, path="/race_stats", name="Race Stats")


q = Queries()

def create_pole_chart():
    pole = q.polePosition()
    
    pass

# page 1 data
df = px.data.gapminder()

layout = html.Div(
    [
        dbc.Row(
            [
                html.H3(
                    children="Life expectancy over the years(1950 - Present)",
                    style={"textAlign": "center"},
                ),
                # dcc.Dropdown(df.country.unique(), "Canada", id="dropdown-selection"),
                # dcc.Graph(id="graph-content"),
                dbc.Col(
                    [dcc.Dropdown(options=df.continent.unique(), id="cont-choice")],
                    xs=10,
                    sm=10,
                    md=8,
                    lg=4,
                    xl=4,
                    xxl=4,
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(
                            id="line-fig",
                            figure=px.histogram(
                                df, x="continent", y="lifeExp", histfunc="avg"
                            ),
                        )
                    ],
                    width=12,
                )
            ]
        ),
    ]
)


@callback(Output("line-fig", "figure"), Input("cont-choice", "value"))
def update_graph(value):
    if value is None:
        fig = px.histogram(df, x="continent", y="lifeExp", histfunc="avg")
    else:
        dff = df[df.continent == value]
        fig = px.histogram(dff, x="country", y="lifeExp", histfunc="avg")
    return fig


# @callback(Output("graph-content", "figure"), Input("dropdown-selection", "value"))
# def update_gapminder(value):
# 	dff = df[df.country == value]
# 	return px.line(dff, x="year", y="pop")
