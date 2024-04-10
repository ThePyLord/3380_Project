import dash
from dash import dcc, html, callback, Output, Input, State, dash_table
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from queries import Queries

dash.register_page(__name__, path="/race_stats", name="Race Stats")

q = Queries()
year = 2006
gp_choice = "Canadian Grand Prix"
grand_prixs = q.grand_prixs(year)
drivers_at_gp = q.drivers_at_gp(year, gp_choice)
circuits = q.circuits()
# Drop circuits with missing lat/lng values or missing elevation data
circs = circuits.copy().dropna(subset=["lat", "lng", "elevation"])
# Set the elevation to an absolute value, but keep the original for hover text
circs["adj_elevation"] = circs["elevation"]
circs.loc[:, "adj_elevation"] = (
    circs.loc[:, "elevation"] - circs.loc[:, "elevation"].min() + 1
)

# circs_
circs_on_map = px.scatter_geo(
    circs,
    lat="lat",
    lon="lng",
    hover_name="name",
    size="adj_elevation",
    color="elevation",
    projection="natural earth",
)


def create_line_progression(params=[2006, "Canadian Grand Prix", "Kimi Räikkönen"]):
    print(params)
    lap_progression = q.lap_time_progression(params[0], params[1], params[2])

    fig = px.line(
        lap_progression,
        x="lap",
        y="time",
        # color="constructor",
        markers=True,
        # symbol="constructor",
    )

    fig.update_layout(
        autosize=True,
        margin=dict(t=50),
        yaxis_title="Time (s)",
        xaxis_title="Laps completed",
        xaxis_type="category",
        title=f"Lap time progression for {params[2]} in the {params[1]} of {params[0]}",
    )

    return fig


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
lap_progression = create_line_progression()

layout = html.Div(
    [
        dbc.Row(
            [
                html.H3(
                    children="Drivers with the most pole positions",
                    style={"textAlign": "center"},
                ),
                dcc.Graph(
                    id="graph-content",
                    figure=pole_pos_chart,
                ),
                html.Div(
                    children=[
                        "The chart above shows the drivers with the most pole positions in Formula 1 history."
                    ],
                    style={"textAlign": "center"},
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
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Dropdown(
                            options=q.years()["year"],
                            id="year-select",
                            placeholder="Select the year",
                        ),
                    ]
                ),
                dbc.Col([dcc.Dropdown(options=grand_prixs["name"], id="gp-choice")]),
                dbc.Col(
                    [
                        dcc.Dropdown(
                            options=drivers_at_gp["driverName"], id="gp-choice-2"
                        )
                    ]
                ),
                dbc.Col(
                    [
                        html.Button(
                            "Submit",
                            id="submit-button",
                            className="btn btn-outline-primary",
                            n_clicks=0,
                        ),
                    ]
                ),
            ],
            justify="center",
        ),
        dbc.Row(
            [
                dcc.Graph(id="line-fig", figure=lap_progression),
            ]
        ),
    ]
)


# @callback(Output("graph-content", "figure"), Input("cont-choice", "value"))
# def update_gapminder(value):
# 	dff = df[df.country == value]
# 	return px.line(dff, x="year", y="pop")


@callback(Output("gp-choice", "options"), Input("year-select", "value"))
def update_gp_options(year):
    if year is None:
        year = 2006
    gp = q.grand_prixs(year)
    return gp["name"]


@callback(
    Output("gp-choice-2", "options"),
    Input("year-select", "value"),
    Input("gp-choice", "value"),
)
def update_driver_options(year, gp):
    if year is None and gp is None:
        year = 2006
        gp = "Canadian Grand Prix"
    drivers = q.drivers_at_gp(year, gp)
    return drivers["driverName"]


@callback(
    [
        Output("line-fig", "figure"),
        Output("year-select", "value"),
        Output("gp-choice", "value"),
        Output("gp-choice-2", "value"),
    ],
    Input("submit-button", "n_clicks"),
    State("year-select", "value"),
    State("gp-choice", "value"),
    State("gp-choice-2", "value"),
)
def update_line_chart(n_clicks, year, gp, driver):
    if n_clicks == 0 or year is None or gp is None or driver is None:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update
    lap_progression = create_line_progression([year, gp, driver])
    return lap_progression, None, None, None
