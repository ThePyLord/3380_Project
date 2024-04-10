import dash
from dash import dcc, html, callback, Output, Input, dash_table, State
import numpy as np
import plotly.express as px
import dash_bootstrap_components as dbc
from queries import Queries

dash.register_page(__name__, path="/performance")

q = Queries()

# Assuming const_pts is your DataFrame and is already defined
year = 2021
driver_year = 2021
teams = ["ferrari", "mercedes"]
constructors = q.constructors()


def create_driver_table(year=2021):
    driver_pts = q.driverPoints(year)
    fig = px.bar(
        driver_pts,
        x="Driver Name",
        y="Points",
        color="Driver Name",
        text="Points",
    )
    fig.update_traces(texttemplate="%{text}", textposition="outside")

    # Update traces to show text above bars
    for trace in fig.data:
        trace.text = trace.y
        trace.textposition = "outside"
        trace.textfont.color = trace.marker.color
    # Optionally, update the layout to adjust the space so that the text fits well
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode="hide")
    return fig


def create_const_table(year=2021):
    const_pts = q.constructorPoints(year)
    fig = px.bar(
        const_pts,
        x="Constructor Name",
        y="Points",
        color="Constructor Name",
        text="Points",
    )

    # Update traces to show text above bars
    for trace in fig.data:
        trace.text = trace.y
        trace.textposition = "outside"
        trace.textfont.color = trace.marker.color
    # Optionally, update the layout to adjust the space so that the text fits well
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode="hide")
    return fig


def create_const_diff(teams=["ferrari", "mercedes"]):
    const_diff = q.compareConstructorPerformance(teams[0], teams[1])

        # print(const_diff.head())
    fig = px.line(
        const_diff,
        x="year",
        y="total_points",
        color="constructor",
        markers=True,
        symbol="constructor",
    )

    fig.update_layout(
        autosize=True,
        margin=dict(t=50),
        yaxis_title="Total Points",
        xaxis_title="Year",
        xaxis_type="category",
    )

    return fig



sprint_table = q.sprint_results()
fig = create_const_table()
driver_fig = create_driver_table()
const_diff = create_const_diff(teams)

layout = html.Div(
    [
        dbc.Row(
            [
                html.H3(
                    children=f"Constructor standings in {year}",
                    style={"textAlign": "center"},
                    id="constructor-title",
                ),
                dbc.Col(
                    [dcc.Dropdown(options=np.arange(1950, 2023 + 1), id="year-choice")],
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
                            id="bar-fig",
                            figure=fig,
                        ),
                        dbc.Row(
                            [
                                html.Caption(
                                    "The bar chart above shows the points won by constructors in the selected year(Excludes constructors with 0 points).",
                                    style={
                                        "textAlign": "center",
                                        "fontStyle": "italic",
                                        "fontSize": "small",
                                    },
                                )
                            ]
                        ),
                    ],
                    width=12,
                ),
                html.Hr(),
                dbc.Row(
                    [
                        html.H3(
                            children=f"Driver Points in {driver_year}",
                            style={"textAlign": "center"},
                            id="driver-title",
                        ),
                        dbc.Row(
                            [
                                dcc.Dropdown(
                                    options=np.arange(1950, 2023 + 1),
                                    id="year-choice-driver",
                                )
                            ],
                        ),
                        dbc.Col(
                            [
                                dcc.Graph(
                                    id="driver-fig",
                                    figure=driver_fig,
                                ),
                                dbc.Row(
                                    [
                                        html.Caption(
                                            "The bar chart above shows the points won by drivers in the selected year(Excludes drivers that didn't get any points).",
                                            style={
                                                "textAlign": "center",
                                                "fontStyle": "italic",
                                                "fontSize": "small",
                                            },
                                        )
                                    ]
                                ),
                            ],
                            width=12,
                        ),
                    ],
                    justify="center",
                ),
                html.Hr(),
                dbc.Row(
                    [
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Row(
                                            [
                                                html.H3(
                                                    id="const_diff_title",
                                                    children="Ferrari v. Mercedes Performance Difference",
                                                    style={"textAlign": "center"},
                                                ),
                                            ]
                                        )
                                    ]
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dcc.Dropdown(
                                                    options=[
                                                        {
                                                            "label": row["constructor"],
                                                            "value": row[
                                                                "constructor"
                                                            ],
                                                        }
                                                        for index, row in constructors.iterrows()
                                                    ],
                                                    placeholder="Select constructor 1",
                                                    id="team-choice-1",
                                                ),
                                            ],
                                            # width=10,
                                        ),
                                        dbc.Col([
                                            dcc.Dropdown(
                                                options=[
                                                    {
                                                        "label": row["constructor"],
                                                        "value": row[
                                                            "constructor"
                                                        ],
                                                    }
                                                    for index, row in constructors.iterrows()
                                                ],
                                                placeholder="Select constructor 2",
                                                id="team-choice-2",
                                            ),
                                        ]),
                                        dbc.Col(
                                            [
                                                html.Button(
                                                    id="submit-button",
                                                    className="btn btn-outline-primary",
                                                    n_clicks=0,
                                                    children="Submit",
                                                ),
                                            ],
                                            width=1,
                                        ),
                                        dcc.Graph(
                                            id="const_diff_plot_2", figure=const_diff
                                        ),
                                        html.P(["The line chart above shows the performance difference between the selected constructors."], style={"textAlign": "center"}),
                                        html.P(["The x-axis represents the year, and the y-axis represents the total points won by the constructors per year."],
                                            style={"textAlign": "center"}),
                                    ],
                                    justify="center",
                                ),
                            ]
                        ),
                    ],
                    justify="center",
                ),
                dbc.Row(
                    [
                        html.H3(
                            children="Number of sprint races won by drivers (all time)",
                            style={"textAlign": "center"},
                        ),
                        dbc.Col(
                            [
                                html.Div(
                                    children=[
                                        "Sprint races only started in 2021, so the data is only available from then.",
                                        # "The table below shows drivers who have won sprint races and the number of wins.",
                                    ],
                                    style={"textAlign": "center"},
                                ),
                                dash_table.DataTable(
                                    id="const-table",
                                    columns=[
                                        {"name": i, "id": i}
                                        for i in sprint_table.columns
                                    ],
                                    data=sprint_table.to_dict("records"),
                                    page_size=10,
                                ),
                            ],
                            style={
                                "display": "flex",
                                "justify-content": "center",
                                "align-items": "center",
                                "flex-direction": "column",
                            },
                        ),
                    ],
                    justify="center",
                    style={"margin-bottom": "20%"},
                ),
            ],
        ),
    ]
)


@callback(Output("bar-fig", "figure"), Input("year-choice", "value"))
def update_const_graph(value=2021):
    if value is None:
        value = 2021
    global year
    year = value
    const_pts = q.constructorPoints(value)
    fig = px.bar(
        const_pts,
        x="Constructor Name",
        y="Points",
        color="Constructor Name",
        text="Points",
    )

    # Update the text on the bars to display the y-value (Points)
    fig = create_const_table(value)
    fig.update_layout(autosize=True, margin=dict(t=50))

    return fig


@callback(Output("constructor-title", "children"), Input("year-choice", "value"))
def update_title(year=2021):
    if year is None:
        year = 2021
    return f"Constructor standings in {year}"


@callback(Output("driver-fig", "figure"), Input("year-choice-driver", "value"))
def update_driver_graph(value=2021):
    if value is None:
        value = 2021
    global driver_year
    driver_year = value
    driver_pts = q.driverPoints(value)
    fig = px.bar(
        driver_pts, x="Driver Name", y="Points", color="Driver Name", text="Points"
    )

    # Update the text on the bars to display the y-value (Points)
    fig = create_driver_table(value)
    fig.update_layout(autosize=True, margin=dict(t=50))

    return fig


@callback(Output("driver-title", "children"), Input("year-choice-driver", "value"))
def update_driver_title(year=2021):
    if year is None:
        year = 2021
    return f"Driver standings in {year}"


@callback(Output("team-choice-1", "options"), Input("team-choice-2", "value"))
def update_team_choice_1(value):
    if value is None:
        teams = q.constructors()
    else:
        print(f"Team choice 2: {value}")
        teams = q.co_competitors(value)
        # dash.no_update
    opts = [
        {"label": row["constructor"], "value": row["constructor"]}
        for _, row in teams.iterrows()
    ]
    return opts


@callback(Output("team-choice-2", "options"), Input("team-choice-1", "value"))
def update_team_choice_2(value):
    if value is None:
        teams = q.constructors()
    else:
        print(f"Team choice 1: {value}")
        teams = q.co_competitors(value)
    opts = [
        {"label": row["constructor"], "value": row["constructor"]}
        for _, row in teams.iterrows()
    ]
    return opts


@callback(
    [
        Output("const_diff_plot_2", "figure"),
        Output("const_diff_title", "children"),
        Output("team-choice-1", "value"),
        Output("team-choice-2", "value"),
    ],
    Input("submit-button", "n_clicks"),
    State("team-choice-1", "value"),
    State("team-choice-2", "value"),
)
def update_const_diff_plot(n_clicks, team1: str, team2: str):
    if n_clicks == 0 or team1 is None or team2 is None:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update
    teams = [team1, team2]
    # print(f'Team 1: {team1}, Team 2: {team2}')
    const_diff = create_const_diff(teams)
    print(f'Team 1: {team1}, Team 2: {team2}')
    return (
        const_diff,
        f"{team1} v. {team2} Performance Difference",
        None,
        None,
    )
