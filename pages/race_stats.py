import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
from queries import Queries


dash.register_page(__name__, path="/race_stats", name="Race Stats")


q = Queries()

def create_pole_chart():
    pole = q.polePositions()
    fig = px.bar(
        pole,
        y="Driver Name",
        x="PolePositions",
        color="Driver Name",
        # text="PolePositions",
        # orientation="h",
    )

    for trace in fig.data:
        trace.text = trace.y
        trace.textposition = "outside"
        trace.textfont.color = trace.marker.color
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode="hide")
    fig.update_layout(autosize=False, margin=dict(t=50))

    return fig


def create_circuit_qual_time():
    qual_time = q.fastestQualifyingTimesByCircuit()
    fig = px.bar(
        qual_time,
        x="circuit_name",
        y="fastest_qualifying_time",
        color="circuit_name",
    )
    
    pass

# page 1 data
df = px.data.gapminder()
pole_pos_chart = create_pole_chart()
layout = html.Div(
    [
        dbc.Row(
            [
                html.H3(
                    children="Drivers with the most pole positions",
                    style={"textAlign": "center"},
                ),
                dbc.Col(
                    [
                        dcc.Graph(
                            id="graph-content",
                            figure=pole_pos_chart,
                        ),
                    ],
                    xs=7,
                    sm=7,
                    align="center",
                ),
                # dcc.Graph(
                #     id="graph-content", figure=pole_pos_chart, style={"height": "100%"}
                # ),
                html.Div(
                    children=[
                        "The chart above shows the drivers with the most pole positions in Formula 1 history."
                    ]
                ),
                dbc.Col(
                    [dcc.Dropdown(options=df.continent.unique(), id="cont-choice")],
                    xs=10,
                    sm=10,
                    md=8,
                    lg=4,
                    xl=4,
                    xxl=4,
                ),
            ],
            justify="center",
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


# @callback(Output("graph-content", "figure"), Input("cont-choice", "value"))
# def update_gapminder(value):
# 	dff = df[df.country == value]
# 	return px.line(dff, x="year", y="pop")
