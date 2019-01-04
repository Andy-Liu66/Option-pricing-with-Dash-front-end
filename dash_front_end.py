import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_reusable_components as drc
import dash_table
import numpy as np
import pandas as pd
from formula import Black_Schole_model, Binomial_model

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    # left div
    html.Div([
        drc.Card([
            html.H4('Black Schole Model and Binomial Model'),
            "Stock price", html.Br(),
            dcc.Input(placeholder="enter stock price", type='number', value=100, id='s'),
            html.Br(),
            "Strike price", html.Br(),
            dcc.Input(placeholder="enter strike price", type='number', value=70, id='k'),
            html.Br(),
            "Volatility (percentage)", html.Br(),
            dcc.Input(placeholder="enter volatiltiy", type='number', value=0.2, id='vol'),
            html.Br(),
            "Risk free rate (percentage)", html.Br(),
            dcc.Input(placeholder='enter rsik free rate', type='number', value=0.01, id='r'),
            html.Br(),
            "Time to maturity (in year)", html.Br(),
            dcc.Input(placeholder='enter time to maturity', type='number', value=1, id='T'),
            html.Br(),
            "Simulation period of Binomial Model", html.Br(),
            dcc.Input(placeholder='enter simulation period', type='number', value=100, id='n_period')
        ])
    ], className='six columns', style={'margin':10}),

    # right div
    html.Div([
        drc.Card([
            html.H4('Output'),

            html.H5('Black Schole Model'),
            html.Div(id='bs_output'),
            html.Br(),

            html.H5('Binomial Model (European)'),
            html.Div(id='binomial_output_eu'),
            html.Br(),

            html.H5('Binomial Model (American)'),
            html.Div(id='binomial_output_us')
        ])
    ], className='six columns', style={'margin':10})
])

# deal with bs_output
@app.callback(
    Output('bs_output', 'children'),
    [Input('s', 'value'),
     Input('k', 'value'),
     Input('vol', 'value'),
     Input('r', 'value'),
     Input('T', 'value')]
)

def update_bs_output(s, k, vol, r, T):
    bs_model = Black_Schole_model(s, k, vol, r, T)
    result = pd.DataFrame([[bs_model.call_price(),
                            bs_model.put_price()]],
                            columns=["Call price", "Put price"])

    table = dash_table.DataTable(id='table',
                                 columns=[{"name": i, "id": i} for i in result.columns],
                                 data=result.to_dict("rows"))

    return table

# deal with binomial_output_eu
@app.callback(
    Output('binomial_output_eu', 'children'),
    [Input('s', 'value'),
     Input('k', 'value'),
     Input('vol', 'value'),
     Input('r', 'value'),
     Input('T', 'value'),
     Input('n_period', 'value')]
)

def update_binomial_output_eu(s, k, vol, r, T, n_period):
    binomial_model_eu = Binomial_model(s, k, vol, r, T, n_period, american=False)
    result = pd.DataFrame([[binomial_model_eu.call_price(),
                            binomial_model_eu.put_price()]],
                            columns=["Call price", "Put price"])

    table = dash_table.DataTable(id='table',
                                 columns=[{"name": i, "id": i} for i in result.columns],
                                 data=result.to_dict("rows"))

    return table

# deal with binomial_output_us
@app.callback(
    Output('binomial_output_us', 'children'),
    [Input('s', 'value'),
     Input('k', 'value'),
     Input('vol', 'value'),
     Input('r', 'value'),
     Input('T', 'value'),
     Input('n_period', 'value')]
)

def update_binomial_output_eu(s, k, vol, r, T, n_period):
    binomial_output_us = Binomial_model(s, k, vol, r, T, n_period, american=True)
    result = pd.DataFrame([[binomial_output_us.call_price(),
                            binomial_output_us.put_price()]],
                            columns=["Call price", "Put price"])

    table = dash_table.DataTable(id='table',
                                 columns=[{"name": i, "id": i} for i in result.columns],
                                 data=result.to_dict("rows"))

    return table

# app.css.append_css({'external_url': 'https://codepen.io/plotly/pen/EQZeaW.css'})
if __name__ == '__main__':
    app.run_server(debug=True)