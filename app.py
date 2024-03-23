from dash import Dash, html, dcc, callback, Output, Input
import dash
import dash_bootstrap_components as dbc
import numpy as np
import plotly.express as px
import pandas as pd
from queries import Queries

q = Queries()

df = pd.read_csv(
	"https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv"
)


app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SPACELAB])

sidebar = dbc.Nav(
    [
        dbc.NavLink(
            [
                html.Div(page["name"], className="ms-2"),
            ],
            href=page["path"],
            active="exact",
        )
        for page in dash.page_registry.values()
    ],
    vertical=True,
    pills=True,
    className="bg-light border-end",
)

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        "COMP 3380 FINAL PROJECT",
                        style={"fontSize": 50, "textAlign": "center"},
                    )
                )
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col([sidebar], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),
                dbc.Col([dash.page_container], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10),
            ]
        ),
		# html.Footer(
		# 	[
		# 		html.P("Our Dash-SQL interface", style={"textAlign": "center", "fontWeight": "bold"}),
		# 		html.P("Created by Victor N. and Ebere O.", style={"textAlign": "center"}),
		# 	],
		# 	className="bg-light text-center text-lg-start",
		# 	style={"position": "fixed", "bottom": 0, "width": "100%"},
		# ),
    ],
    fluid=True,
)


# app.layout = html.Div(
#     [
#         # html.H1(children="Population growth over the years(1950 - Present)", style={"textAlign": "center"}),
#         # dcc.Dropdown(df.country.unique(), "Canada", id="dropdown-selection"),
#         # dcc.Graph(id="graph-content"),
#         html.H1(
#             id="constructor-title",
#             children=f"Points won by Constructors in {year}",
#             style={"textAlign": "center"},
#         ),
#         dcc.Dropdown(np.arange(1950, 2022), 2021, id="dropdown-selection-2"),
#         dcc.Graph(id="graph-content-2", figure=fig),
#         # dcc.Link(page) for page in dash.page
#     ]
# )


# @callback(
#     Output("constructor-title", "children"), Input("dropdown-selection-2", "value")
# )
# def update_title(year):
#     return f"Points won by Constructors in {year}"





# @callback(Output("graph-content-2", "figure"), Input("dropdown-selection-2", "value"))
# def update_graph_2(value = 2021):
#     global year
#     year = value
#     const_pts = q.constructorPoints(value)
#     fig = px.bar(const_pts, x="name", y="Points", color="name", text="Points")

#     # Update the text on the bars to display the y-value (Points)
#     fig.update_traces(texttemplate="%{text}", textposition="outside")

#     for trace in fig.data:
#         trace.marker.color = (
#             trace.marker.color
#         )  # Ensure the marker color is explicitly set for clarity
#         trace.textfont.color = trace.marker.color

#     # Optionally, adjust the layout to make sure there is enough room for text labels above bars
#     fig.update_layout(
#         autosize=True, margin=dict(t=50)
#     )  # Increase top margin to ensure labels fit

#     return fig


if __name__ == "__main__":
	app.run(debug=True)
	# app.run()
