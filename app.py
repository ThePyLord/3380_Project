from dash import Dash, html, dcc, callback, Output, Input
import numpy as np
import plotly.express as px
import pandas as pd
from queries import Queries

q = Queries()
const_pts = q.constructorPoints(2021)


df = pd.read_csv(
	"https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv"
)

app = Dash(__name__)

app.layout = html.Div(
	[
		html.H1(children="Population growth over the years(1950 - Present)", style={"textAlign": "center"}),
		dcc.Dropdown(df.country.unique(), "Canada", id="dropdown-selection"),
		dcc.Graph(id="graph-content"),
		html.H1(children="Points won by Constructors in 2021", style={"textAlign": "center"}),
		dcc.Graph(id="graph-content-2", figure=px.bar(const_pts, x="name", y="Points", color="name")),
		dcc.Dropdown([np.arange(1950, 2022)], 2021, id="dropdown-selection-2"),
		# dcc.Link(page) for page in dash.page
	]
)

@callback(Output("graph-content", "figure"), Input("dropdown-selection", "value"))
def update_graph(value):
	dff = df[df.country == value]
	return px.line(dff, x="year", y="pop")

# @callback(Output("graph-content-2", "figure"), Input("dropdown-selection", "value"))
def update_graph_2(value = 2021):
	const_pts = q.constructorPoints(value)
	return px.bar(const_pts, x="name", y="Points", color="name")


if __name__ == "__main__":
	app.run(debug=True)
