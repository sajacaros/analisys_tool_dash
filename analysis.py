import plotly
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.FLATLY]  # CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

app.layout = dbc.Container([
    dbc.Container([
        dbc.Row([
            dbc.Col(
                dbc.RadioItems(
                    options={
                        'csv': 'csv url',
                        'seaborn': 'seaborn data',
                        'plotly': 'plotly data',
                        'sklearn': 'sklearn data',
                    },
                    value='csv',
                ),
            ),
            dbc.Col(html.Div('world'), style={'backgroundColor': 'red'}),
            dbc.Col(html.Div('!!!'), style={'backgroundColor': 'blue'}),
        ]),
        dbc.Row(html.Div('chart'), style={'backgroundColor': 'yellow'}),
    ]),
])

if __name__=='__main__':
    app.run(debug=True)
