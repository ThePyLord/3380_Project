import dash
from dash import dcc, html, callback, Output, Input, dash_table
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from queries import Queries

dash.register_page(__name__, path="/race_stats", name="Race Stats")

q = Queries()
circuits = q.circuits()
# Drop circuits with missing lat/lng values or missing elevation data
circs = circuits.copy().dropna(subset=["lat", "lng", "elevation"])
# Set the elevation to an absolute value, but keep the original for hover text
circs["adj_elevation"] = circs["elevation"]
circs.loc[:, "adj_elevation"] = circs.loc[:, "elevation"] - circs.loc[:, "elevation"].min() + 1

# circs_
circs_on_map = px.scatter_geo(circs, lat="lat", lon="lng", hover_name="name", size="adj_elevation", color="elevation", projection="natural earth")

def create_pole_chart():
	pole = q.polePositions()
	fig = px.bar(
		pole,
		x="Driver Name",
		y="PolePositions",
		color="Driver Name",
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
    circuits = q.circuits()

    fig = px.box(
        qual_time,
        x="circuit_name",
        y="fastest_qualifying_time",
        color="circuit_name",
    )

    # for trace in fig.data:
    #     trace.text = trace.y
    #     trace.textposition = "outside"
    #     trace.textfont.color = trace.marker.color

    fig.update_layout(uniformtext_minsize=8, uniformtext_mode="hide")
    fig.update_layout(
        autosize=True,
        margin=dict(t=50),
        xaxis_title="Circuit",
        yaxis_title="Fastest Qualifying Time (s)",
    )

    return fig


def create_sprint_table():
    sprint_results = q.sprint_results()
    fig = px.bar(
        sprint_results,
        x="Driver Name",
        y="Points",
        color="Driver Name",
        text="Points",
    )

    for trace in fig.data:
        trace.text = trace.y
        trace.textposition = "outside"
        trace.textfont.color = trace.marker.color

    fig.update_layout(uniformtext_minsize=8, uniformtext_mode="hide")
    return fig


pole_pos_chart = create_pole_chart()
qual_chart = create_circuit_qual_time()

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
                        html.Div(
                            children=[
                                "The chart above shows the drivers with the most pole positions in Formula 1 history."
                            ]
                        ),
                    ],
                    xs=7,
                    sm=7,
                    align="center",
                ),
            ],
            justify="center",
        ),
        html.Hr(),
        dbc.Row(
            [
                html.H3(
                    children="Fastest Qualifying Times By Circuit",
                    style={"textAlign": "center"},
                ),
                dbc.Col(
                    [
                        dcc.Graph(id="qual-chart", figure=qual_chart),
                    ],
                    # width=12,
                )
            ]
        ),
    ]
)


# @callback(Output("graph-content", "figure"), Input("cont-choice", "value"))
# def update_gapminder(value):
# 	dff = df[df.country == value]
# 	return px.line(dff, x="year", y="pop")
