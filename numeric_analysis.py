import dash_bootstrap_components as dbc
import plotly.express as px
from dash import html, dcc, Output, Input
import plotly.figure_factory as ff

def numeric_analysis(app):
    return NumericAnalysis(app)


from abc import ABCMeta, abstractmethod


class BaseBlock(metaclass=ABCMeta):
    def __init__(self, app=None, prefix=''):
        self.app = app
        self.prefix = prefix
        self._data = None
        self._numeric_columns = None

        if self.app is not None and hasattr(self, 'callbacks'):
            self.callbacks(self.app)
            print(prefix, ' init analysis')

    @abstractmethod
    def callbacks(self, app):
        pass

    def change_data(self, df):
        self._data = df
        self._numeric_columns = self._data.select_dtypes('number').columns


class NumericAnalysis(BaseBlock):
    def __init__(self, app):
        super().__init__(app, 'Numeric')

    def callbacks(self, app):
        @app.callback(
            Output('box-graph', 'figure'),
            [Input('select_column_num', 'value')],
        )
        def change_page_box(page):
            selected_column = self._numeric_columns[page]
            fig = px.box(self._data,y=selected_column)
            fig.update_layout(
                title={
                    'text': f"{selected_column}'s Box",
                    'y': 0.95,
                    'x': 0.5,
                },
            )
            return fig

        @app.callback(
            Output('describe-text', 'children'),
            [Input('select_column_num', 'value')],
        )
        def change_page_describe(page):
            selected_column = self._numeric_columns[page]
            s = self._data[selected_column].describe()
            return [dbc.Row([dbc.Col(column, className='text-center'), dbc.Col(round(v,2))]) for column, v in zip(s.index, s)]

    def render(self):
        return dbc.Card(
            dbc.CardBody(
                dbc.Row([
                    dbc.Col(
                        [
                            dbc.RadioItems(
                                id='select_column_num',
                                className='btn-group',
                                inputClassName='btn-check',
                                labelClassName='btn btn-outline-primary',
                                labelCheckedClassName='active',
                                options=[
                                    {'label': column_name, 'value': idx} for idx, column_name in enumerate(self._numeric_columns)
                                ],
                                value=0,
                                style={'flex-wrap':'wrap'},
                            ),
                        ], width=4, className='bg-light border',
                    ),
                    dbc.Col(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(dcc.Graph(figure={}, id='box-graph', config={'displayModeBar': False}), width=5),
                                    dbc.Col(html.Div(id='describe-text'), width=2, align='start', style={'margin-top': 50, 'display': 'block'}),
                                ],  align='center',
                            ),
                        ], width=8,
                    ),
                ]),
            ),
        )
