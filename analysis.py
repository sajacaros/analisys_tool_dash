import plotly
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import seaborn as sns


external_stylesheets = [dbc.themes.FLATLY]  # CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)


def csv_input(disable=False):
    """
    :param disable:
        if True, input disable
        otherwise, input enable
        default False
    :return:
        csv url by user input
    """
    return html.Div([
        dbc.Input(id='csv_input', placeholder='Type csv url', type='text', disabled=disable),
    ])

def seaborn_datalist():
    """
    :return:
        seaborn data list
    """
    return sns.get_dataset_names()

def plotly_datalist():
    """
    :return:
        plotly data list
    """
    return ['carshare', 'election', 'experiment', 'gapminder', 'iris', 'medals_long', 'medals_wide', 'stocks', 'tips', 'wind']

def sklearn_datalist():
    """
    :return:
        sklearn data list
    """
    return ['iris', 'diabetes', 'digits', 'wine', 'breast_cancer']


def datasource_input(data_source, disable=False):
    """
    serve input box or select box, that select data_source
    :param data_source:
        csv, seaborn, plotly, sklearn
    :param disable:
        if True, select disable
        otherwise, sleect enable
        default False
    :return:
        select input for data_source
    """
    data_list = (
        seaborn_datalist() if data_source == 'seaborn' else
        plotly_datalist() if data_source == 'plotly' else
        sklearn_datalist()
    )
    return html.Div([
        csv_input() if data_source == 'csv' else
        dbc.Select(
            id=data_source+'_input',
            options=[{'label': data, 'value': data} for data in data_list],
            value=data_list[0],
            disabled=disable,
        ),
    ])


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
            dbc.Col([
                dbc.Row(datasource_input('csv')),
                dbc.Row(datasource_input('seaborn')),
                dbc.Row(datasource_input('plotly')),
                dbc.Row(datasource_input('sklearn')),
            ]),
            dbc.Col(dbc.Button('apply', color='primary', className='me-1')),
        ]),
        dbc.Row(html.Div('chart'), style={'backgroundColor': 'yellow'}),
    ]),
])

if __name__=='__main__':
    app.run(debug=True)
