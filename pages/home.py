import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/")

layout = html.Div(
    [
        dbc.Row(
            [
				dbc.Col([
                    html.H1("Welcome to our 3380 FINAL PROJECT!", style={"textAlign": "center"}),
                    html.H3("To enter your input anywhere in the app, please make use of the dropdowns provided.", 
							 style={"textAlign": "center", "fontSize": 20, "fontStyle": "bold"}),
                ]),
            ],
			justify="center",
        ),
		dbc.Row(
			[
				dbc.Col([
                    html.H3("Sitemap. It contains the following pages:"),
                    html.Ul([
                        html.Li("Home: This page."),
						html.Li(dcc.Markdown("**Help: This page contains information on how to use the app. PLEASE [READ THIS FIRST!](/help)**")),
                        html.Li("Miscellaneous Stats: This page contains miscellaneous statistics. For example, the fastest laps."),
                        html.Li("Performance Stats: This page contains statistics on the performance of drivers and constructors."),
                        html.Li("Race Stats: This page contains statistics relating to races or events that happen during races.")
                    ]),
                ]),
            ],
			justify="center",
        ),
		dbc.Row([
			dbc.Col([
				html.Strong([
					"Disclaimer: Some of the results in the app may not be up to date. The data is generally accurate up until August 2023."
                ])
            ]),
        ])
    ]
)
