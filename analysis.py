import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import seaborn as sns
from dash import Dash, html, Output, Input, State
from sklearn import datasets

from numeric_analysis import numeric_analysis

external_stylesheets = [dbc.themes.FLATLY]  # CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)


def csv_input(disable=False):
    """
    :param disable:
        if True, input disable
        otherwise, input enable
        default False
    :return:
        input box for user input
    """
    return dbc.Input(id='data_name_select',type='text', value='https://raw.githubusercontent.com/DSNote/fastcampus/main/rent.csv', disabled=disable)


def select_input(data_source, disable=False):
    """
    :param data_source:
        data source name, seaborn, plotly
    :param disable:
        if True, input disable
        otherwise, input enable
        default False
    :return:
        select box for user input
    """
    data_list = (
        seaborn_datalist() if data_source == 'seaborn' else
        plotly_datalist() if data_source == 'plotly' else
        sklearn_datalist()
    )

    return dbc.Select(
        id='data_name_select',
        options=[{'label': data, 'value': data} for data in data_list],
        value=data_list[0],
        disabled=disable,
    )


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
    return [
        'carshare', 'election', 'experiment', 'gapminder', 'iris', 'medals_long', 'medals_wide', 'stocks', 'tips',
        'wind',
    ]


def sklearn_datalist():
    """
        :return:
            sklearn data list
        """
    return [
        'iris', 'diabetes', 'digits', 'linnerud', 'wine', 'breast_cancer',
    ]


def datasource_input(data_source, disable=False):
    """
    serve input box or select box, that select data_source
    :param data_source:
        csv, seaborn, plotly
    :param disable:
        if True, select disable
        otherwise, select enable
        default False
    :return:
        select input for data_source
    """
    return csv_input(disable) if data_source == 'csv' else select_input(data_source, disable)


@app.callback(
    Output(component_id='user_input_component', component_property='children'),
    Input(component_id='datasource_select', component_property='value'),
)
def activate_input_component(target):
    return dbc.Row(datasource_input(target))


numeric_analysis = numeric_analysis(app)


def get_csv_data(data_name):
    return pd.read_csv(data_name)


def get_seaborn_data(data_name):
    return sns.load_dataset(data_name)


def get_plotly_data(data_name):
    return getattr(px.data, data_name)()


def get_sklearn_data(data_name):
    data = getattr(datasets, 'load_'+data_name)()
    df = pd.DataFrame(
        data=data.data,
        columns=data.feature_names,
    )
    df['target'] = pd.Series(data.target)
    return df


def get_data(datasource, data_name):
    """
    :param datasource: data daource
    :param data_name: data name
    :return:
        dataframe for data name
    """
    return (
        get_csv_data(data_name) if datasource == 'csv' else
        get_seaborn_data(data_name) if datasource == 'seaborn' else
        get_plotly_data(data_name) if datasource == 'plotly' else
        get_sklearn_data(data_name)
    )


@app.callback(
    Output(component_id='analysis_area', component_property='children'),
    Input(component_id='apply_submit', component_property='n_clicks'),
    State(component_id='datasource_select', component_property='value'),
    State(component_id='data_name_select', component_property='value'),
    prevent_initial_call=True,
)
def apply_datasource(n_clicks, datasource, data_name):
    data_df = get_data(datasource, data_name)
    numeric_analysis.change_data(data_df)
    return numeric_analysis.render()


app.layout = dbc.Container([
    dbc.Container([
        dbc.Row(
            [
                dbc.Col(
                    dbc.RadioItems(
                        id='datasource_select',
                        options={
                            'csv': 'csv url',
                            'seaborn': 'seaborn data',
                            'plotly': 'plotly data',
                            'sklearn': 'sklearn data',
                        },
                        value='csv',
                    ),
                    width=2,
                ),
                dbc.Col(html.Div(id='user_input_component'), width=8),
                dbc.Col(
                    dbc.Button(id='apply_submit', children='apply', n_clicks=0, color='primary', className='me-1'), width=2,
                ),
            ], align='center',
        ),
        html.Hr(),
        dbc.Row(html.Div(id='analysis_area'), style={'backgroundColor': 'yellow'}),
    ]),
])

if __name__ == '__main__':
    app.run(debug=True)
