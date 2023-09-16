import plotly
from dash import Dash, html, dcc, callback, Output, Input, State
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
        input box for user input
    """
    return dbc.Input(id='data_name_select',type='text', value='https://raw.githubusercontent.com/DSNote/fastcampus/main/rent.csv', disabled=disable)


def select_input(data_source, disable=False):
    """
    :param data_source:
        data source name, seaborn, plotly, sklearn
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
    return ['iris', 'diabetes', 'digits', 'wine', 'breast_cancer']


def datasource_input(data_source, disable=False):
    """
    serve input box or select box, that select data_source
    :param data_source:
        csv, seaborn, plotly, sklearn
    :param disable:
        if True, select disable
        otherwise, select enable
        default False
    :return:
        select input for data_source
    """
    return csv_input(disable) if data_source == 'csv' else select_input(data_source, disable)

input_types = ['csv', 'seaborn', 'plotly', 'sklearn']
@app.callback(
    Output(component_id='user_input_component', component_property='children'),
    Input(component_id='datasource_select', component_property='value'),
)
def activate_input_component(target):
    return dbc.Row(datasource_input(target))

@app.callback(
    Output(component_id='analysis_area', component_property='children'),
    Input(component_id='apply_submit', component_property='n_clicks'),
    State(component_id='datasource_select', component_property='value'),
    State(component_id='data_name_select', component_property='value'),
    prevent_initial_call=True,
)
def apply_datasource(n_clicks, datasource, data_name):
    # data_df = get_data(datasource)
    # data_df.head()
    print(datasource)
    return html.Div(f'{datasource}, {data_name}')


app.layout = dbc.Container([
    dbc.Container([
        dbc.Row([
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
            ),
            dbc.Col(html.Div(id='user_input_component')),
            dbc.Col(dbc.Button(id='apply_submit', children='apply', n_clicks=0, color='primary', className='me-1')),
        ]),
        dbc.Row(html.Div(id='analysis_area'), style={'backgroundColor': 'yellow'}),
    ]),
])

if __name__ == '__main__':
    app.run(debug=True)
