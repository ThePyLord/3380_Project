import dash
from dash import dcc, html, callback, Output, Input, dash_table
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
    )

    return fig

def create_line_progression(params=[2009,"Australian Grand Prix","Lewis","Hamilton"]):
    const_diff = q.lap_time_progression(params[0], params[1],params[2],params[3])
    fig = px.line(
        const_diff,
        x="Laps",
        y="Seconds",
        color="constructor",
        markers=True,
        symbol="constructor",
    )

    fig.update_layout(
        autosize=True,
        margin=dict(t=50),
        yaxis_title="Seconds",
        xaxis_title="Laps",
    )

    return fig

# fig = px.bar(q.constructorPoints(year), x="Constructor Name", y="Points", color="Constructor Name")
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
                        dbc.Col(
                            [
                                dcc.Dropdown(
                                    options=np.arange(1950, 2023 + 1),
                                    id="year-choice-driver",
                                )
                            ],
                            xs=10,
                            sm=10,
                            md=8,
                            lg=4,
                            xl=4,
                            xxl=4,
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
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H3(
                                    children="Performance Difference between Ferrari and Mercedes",
                                    style={"textAlign": "center"},
                                ),
                                dbc.Row([dcc.Dropdown(options = constructors.loc[:, 'constructor'], id="team-choice", value=teams, multi=True)]),
                                dcc.Graph(id="const_diff_plot", figure=const_diff),
                            ]
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        html.H3(
                            children="Number of sprint races won by drivers (all time)",
                            style={"textAlign": "center"},
                        ),
                        dash_table.DataTable(
                            id="const-table",
                            columns=[
                                {"name": i, "id": i} for i in sprint_table.columns
                            ],
                            data=sprint_table.to_dict("records"),
                            page_size=10,
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


@callback(Output("const_diff_plot", "figure"), Input("year-choice", "value"))
def update_const_diff_plot(value=2021):
	if value is None:
		value = 2021
	const_diff = create_const_diff(teams)
	return const_diff
