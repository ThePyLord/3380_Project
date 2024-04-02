import dash
from dash import dcc, html, callback, Output, Input, dash_table
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from queries import Queries

dash.register_page(__name__, path="/miscellaneous", name="Miscellaneous Stats")

q = Queries()
fastest_laps = q.fastestLaps()
circuits = q.circuits()
ret_df = q.causes_of_retirements()
retirements = q.causes_of_retirements()

def create_circ_map():
    # Drop circuits with missing lat/lng values or missing elevation data
    circs = circuits.copy().dropna(subset=["lat", "lng", "elevation"])
    # Set the elevation to an absolute value, but keep the original for hover text
    circs["adj_elevation"] = circs["elevation"]
    circs.loc[:, "adj_elevation"] = (
        circs.loc[:, "elevation"] - circs.loc[:, "elevation"].min() + 1
    )

    circs_on_map = px.scatter_geo(
        circs,
        lat="lat",
        lon="lng",
        hover_name="name",
        size="adj_elevation",
        color="elevation",
        projection="natural earth",
    )

    # Update the layout
    circs_on_map.update_layout(
        title="Elevations of circuits on the map\n(in metres above sea level)",
        # centre the title
        title_x=0.5,
        geo=dict(projection=dict(type="natural earth")),
    )

    circs_on_map.update_geos(showcountries=True)

    return circs_on_map


def create_retirement_plot():
    retirements = q.causes_of_retirements()
    fig = px.pie(
        retirements,
        values="retirements",
        names="circuit",
    )
    return fig


circs_on_map = create_circ_map()
retirements = create_retirement_plot()

layout = html.Div(
    [
        dbc.Row(
            [html.H1("Miscellaneous Stats")],
        ),
        html.Hr(),
        dbc.Row(
            [
                html.Div(
                    [
                        html.H2("Fastest Laps Table"),
                        dash_table.DataTable(
                            id="fastest_laps_table",
                            columns=[
                                {"name": i, "id": i} for i in fastest_laps.columns
                            ],
                            data=fastest_laps.to_dict("records"),
                            page_size=10,
                        ),
                    ]
                ),
                html.Hr(),
                dbc.Row(
                    [
                        html.H2("Circuits Map with Elevation"),
                        html.Div(
                            className="text-center",
                            children=[
                                html.P(
                                    "Hover over the circuits to see their names and elevations. The size of the circle represents the elevation of the circuit."
                                )
                            ],
                        ),
                        dcc.Graph(figure=circs_on_map),
                    ],
                    style={"textAlign": "center"},
                ),
                html.Hr(),
                dbc.Row(
                    [
                        html.H2(
                            "Distribution of retirements by circuits(%)",
                            style={"textAlign": "center"},
                        ),
                        dcc.Graph(id="ret-id", figure=retirements),
                        html.Footer(children=f"{ret_df.loc[0,'circuit']} has the highest percentage of retirements, at about {ret_df.loc[0,'retirements']}% of all retirements.", style={'textAlign': 'center'}),
                    ],
                ),
            ]
        ),
    ], style={"margin-bottom": "2%"}
)
