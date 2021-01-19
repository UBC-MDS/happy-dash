# Author: Kevin Shahnazari
# Date created: Jan 18 2021

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "12rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

mirco_tab_leftbar_features = dbc.Checklist(
    options=[
        {'label': 'GDP', 'value': 'gdp'},
        {'label': 'Family', 'value': 'family'},
        {'label': 'Health', 'value': 'health'},
        {'label': 'Freedom', 'value': 'freedom'}
    ]
)

mirco_tab_leftbar_countries = dbc.Checklist(
    options=[
        {'label': 'Afghanistan', 'value': 'afghanistan'},
        {'label': 'Albania', 'value': 'Albania'},
        {'label': 'Algeria', 'value': 'algeria'},
        {'label': 'Andorra', 'value': 'andorra'},
        {'label': 'Afghanistan', 'value': 'afghanistan'},
        {'label': 'Albania', 'value': 'Albania'},
        {'label': 'Algeria', 'value': 'algeria'},
        {'label': 'Andorra', 'value': 'andorra'},
        {'label': 'Afghanistan', 'value': 'afghanistan'},
        {'label': 'Albania', 'value': 'Albania'},
        {'label': 'Algeria', 'value': 'algeria'},
        {'label': 'Andorra', 'value': 'andorra'},
        {'label': 'Afghanistan', 'value': 'afghanistan'},
        {'label': 'Albania', 'value': 'Albania'},
        {'label': 'Algeria', 'value': 'algeria'},
        {'label': 'Andorra', 'value': 'andorra'},
        {'label': 'Afghanistan', 'value': 'afghanistan'},
        {'label': 'Albania', 'value': 'Albania'},
        {'label': 'Algeria', 'value': 'algeria'},
        {'label': 'Andorra', 'value': 'andorra'}
    ]
)

sidebar = html.Div(
    [
        html.H2("Features", className="display-6"),
        html.Hr(),
        mirco_tab_leftbar_features,
        html.Hr(),
        html.H3("Year range", className="display-6"),
        dcc.RangeSlider(
            min=2015,
            max=2019,
            step=1,
            marks={
                2015: {'label': '2015'},
                2016: {'label': '16'},
                2017: {'label': '17'},
                2018: {'label': '18'},
                2019: {'label': '2019'},
            },
            value=[2015, 2019],
            #  allowCross=False,
        ),
        html.Hr(),
        html.H3("Countries", className="display-6"),
        dbc.Col(
            html.Div(id='timeline-div',
                     children=[mirco_tab_leftbar_countries]),
            width=12,
            style={'width': '100%',
                   'height': '300px',
                   'overflow': 'scroll',
                   'padding': '10px 10px 10px 0px'
                   }
        ),
    ],
    style=SIDEBAR_STYLE,
)


micro_tab_leftbar = [
    mirco_tab_leftbar_features,
    dbc.Label('Countries'),
]

micro_tab = dbc.Row([
    dbc.Col(micro_tab_leftbar, lg=2, md=2),
    dbc.Col(html.Div(), md=4, lg=4)
])


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([
    # dbc.Tabs([
    #     dbc.Tab(micro_tab, label='Micro', style={'background-color': 'red'}),
    #     dbc.Tab('overall tab', label='Overall')
    # ])
    sidebar,
])


if __name__ == '__main__':
    app.run_server(debug=True)
