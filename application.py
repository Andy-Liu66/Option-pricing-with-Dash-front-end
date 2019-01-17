import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_reusable_components as drc
import dash_table
import plotly.graph_objs as go
import numpy as np
import pandas as pd
from formula import Black_Scholes_model, Binomial_model, Monte_Carlo_simulation

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
application = app.server

app.layout = html.Div(children=[
    # title
    html.H3('Option pricing - Black Scholes Model, Binomial Model, and Monte Carlo Simulation', style={'textAlign': 'center', 'color': '#adb7c9', 'font-size': '2.8vw'}),
    html.Div([
            # left div
            html.Div([
                drc.Card([
                    html.H5('Parameters'),
                    "Stock price", html.Br(),
                    dcc.Input(placeholder="enter stock price", type='number', value=100, id='s', style={'width': '100%'}),
                    html.Br(),
                    "Strike price", html.Br(),
                    dcc.Input(placeholder="enter strike price", type='number', value=70, id='k', style={'width': '100%'}),
                    html.Br(),
                    "Volatility (%)", html.Br(),
                    dcc.Input(placeholder="enter volatiltiy", type='number', value=20, id='vol', style={'width': '100%'}),
                    html.Br(),
                    "Risk free rate (%)", html.Br(),
                    dcc.Input(placeholder='enter rsik free rate', type='number', value=1, id='r', style={'width': '100%'}),
                    html.Br(),
                    "Time to maturity (year)", html.Br(),
                    dcc.Input(placeholder='enter time to maturity', type='number', value=1, id='T', style={'width': '100%'}),
                    html.Br(),
                    "Number of period for Binomial Model", html.Br(),
                    dcc.Input(placeholder='enter simulation period', type='number', value=100, id='n_period_binomial', style={'width': '100%'}),
                    html.Br(),
                    "Number of path for Monte Carlo simulation", html.Br(),
                    dcc.Input(placeholder='enter simulation period', type='number', value=10000, id='n_period_monte_carlo', style={'width': '100%'})
                ])
            ], style={'flex': 1.5, 'vertical-align': 'middle'}),

            # middle div
            html.Div([
                drc.Card([
                    html.H5('Price'),

                    'Black Scholes Model', html.Br(),
                    html.Div(id='bs_output'),
                    # html.Br(),

                    'Binomial Model (European)', html.Br(),
                    html.Div(id='binomial_output_eu'),
                    # html.Br(),

                    'Binomial Model (American)', html.Br(),
                    html.Div(id='binomial_output_us'),

                    'Monte Carlo Simulation', html.Br(),
                    html.Div(id='monte_carlo_output'),

                    html.Br(),
                    html.H5('Other information'),

                    'Black Scholes Model', html.Br(),
                    html.Div(id='bs_info'),
                    # html.Br(),

                    'Binomial Model', html.Br(),
                    html.Div(id='binomial_info')
                ])
            ], style={'flex': 2, 'vertical-align': 'middle'}),

            # right div
            html.Div([
                drc.Card([
                    dcc.Tabs(id="tabs", value='binomial_call', children=[
                        dcc.Tab(label='Convergence of call price', value='binomial_call'),
                        dcc.Tab(label='Convergence of put price', value='binomial_put')
                    ]),
                    html.Div(id='tabs-content')
                ])
            ], style={'flex': 5, 'vertical-align': 'middle'})
    ], style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'center', 'margin': 'auto'})
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
    vol = vol/100
    r = r/100
    bs_model = Black_Scholes_model(s, k, vol, r, T)
    value = [bs_model.call_price(),
             bs_model.put_price()]
    value = list(map(lambda x: np.round(x, 4), value))
    result = pd.DataFrame([value],
                          columns=["Call price", "Put price"])

    table = dash_table.DataTable(id='table',
                                 columns=[{"name": i, "id": i} for i in result.columns],
                                 data=result.to_dict("rows"),
                                 style_cell={'textAlign': 'center'})

    return table

# deal with binomial_output_eu
@app.callback(
    Output('binomial_output_eu', 'children'),
    [Input('s', 'value'),
     Input('k', 'value'),
     Input('vol', 'value'),
     Input('r', 'value'),
     Input('T', 'value'),
     Input('n_period_binomial', 'value')]
)

def update_binomial_output_eu(s, k, vol, r, T, n_period):
    vol = vol/100
    r = r/100
    binomial_model_eu = Binomial_model(s, k, vol, r, T, n_period, american=False)
    value = [binomial_model_eu.call_price(),
             binomial_model_eu.put_price()]
    value = list(map(lambda x: np.round(x, 4), value))
    result = pd.DataFrame([value],
                          columns=["Call price", "Put price"])

    table = dash_table.DataTable(id='table',
                                 columns=[{"name": i, "id": i} for i in result.columns],
                                 data=result.to_dict("rows"),
                                 style_cell={'textAlign': 'center'})

    return table

# deal with binomial_output_us
@app.callback(
    Output('binomial_output_us', 'children'),
    [Input('s', 'value'),
     Input('k', 'value'),
     Input('vol', 'value'),
     Input('r', 'value'),
     Input('T', 'value'),
     Input('n_period_binomial', 'value')]
)

def update_binomial_output_eu(s, k, vol, r, T, n_period):
    vol = vol/100
    r = r/100
    binomial_output_us = Binomial_model(s, k, vol, r, T, n_period, american=True)
    value = [binomial_output_us.call_price(),
             binomial_output_us.put_price()]
    value = list(map(lambda x: np.round(x, 4), value))
    result = pd.DataFrame([value],
                          columns=["Call price", "Put price"])

    table = dash_table.DataTable(id='table',
                                 columns=[{"name": i, "id": i} for i in result.columns],
                                 data=result.to_dict("rows"),
                                 style_cell={'textAlign': 'center'})

    return table

# deal with monte_carlo_output
@app.callback(
    Output('monte_carlo_output', 'children'),
    [Input('s', 'value'),
     Input('k', 'value'),
     Input('vol', 'value'),
     Input('r', 'value'),
     Input('T', 'value'),
     Input('n_period_monte_carlo', 'value')]
)

def update_monte_carlo_output(s, k, vol, r, T, n_simulation):
    vol = vol/100
    r = r/100
    monte_carlo_output = Monte_Carlo_simulation(s, k, vol, r, T, n_simulation)
    value = [monte_carlo_output.call_price(),
             monte_carlo_output.put_price()]
    value = list(map(lambda x: np.round(x, 4), value))
    result = pd.DataFrame([value],
                          columns=["Call price", "Put price"])

    table = dash_table.DataTable(id='table',
                                 columns=[{"name": i, "id": i} for i in result.columns],
                                 data=result.to_dict("rows"),
                                 style_cell={'textAlign': 'center'})

    return table

# deal with bs_info
@app.callback(
    Output('bs_info', 'children'),
    [Input('s', 'value'),
     Input('k', 'value'),
     Input('vol', 'value'),
     Input('r', 'value'),
     Input('T', 'value')]
)

def update_bs_info(s, k, vol, r, T):
    vol = vol/100
    r = r/100
    bs_model = Black_Scholes_model(s, k, vol, r, T)
    value = [bs_model.nd2,
             bs_model.nnd2]
    value = list(map(lambda x: np.round(x, 4), value))
    result = pd.DataFrame([value],
                          columns=["N(d2)", "N(-d2)"])

    table = dash_table.DataTable(id='table',
                                 columns=[{"name": i, "id": i} for i in result.columns],
                                 data=result.to_dict("rows"),
                                 style_cell={'textAlign': 'center'})

    return table

# deal with binomial_info
@app.callback(
    Output('binomial_info', 'children'),
    [Input('s', 'value'),
     Input('k', 'value'),
     Input('vol', 'value'),
     Input('r', 'value'),
     Input('T', 'value'),
     Input('n_period_binomial', 'value')]
)

def update_binomial_info(s, k, vol, r, T, n_period):
    vol = vol/100
    r = r/100
    binomial_model = Binomial_model(s, k, vol, r, T, n_period)
    value = [binomial_model.up,
             binomial_model.down,
             binomial_model.probability]
    value = list(map(lambda x: np.round(x, 4), value))
    result = pd.DataFrame([value],
                          columns=["up", "down", "probability"])

    table = dash_table.DataTable(id='table',
                                 columns=[{"name": i, "id": i} for i in result.columns],
                                 data=result.to_dict("rows"),
                                 style_cell={'textAlign': 'center'})

    return table

# deal with plot
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value'),
               Input('s', 'value'),
               Input('k', 'value'),
               Input('vol', 'value'),
               Input('r', 'value'),
               Input('T', 'value')])

def render_content(tab, s, k, vol, r, T):
    if tab == 'binomial_call':
        return html.Div([
            dcc.Graph(id='graph', figure=generate_figure(tab, s, k, vol, r, T))
        ])
    elif tab == 'binomial_put':
        return html.Div([
            dcc.Graph(id='graph', figure=generate_figure(tab, s, k, vol, r, T))
        ])

def generate_figure(tab, s, k, vol, r, T):
    vol = vol/100
    r = r/100
    bs_model = Black_Scholes_model(s, k, vol, r, T)
    if tab == 'binomial_call':
        price = []
        for i in np.arange(1, 101, 1):
            binomial_model = Binomial_model(s, k, vol, r, T, i)
            price.append(binomial_model.call_price())
        
        trace_bs = go.Scatter(
            x = np.arange(1, 101, 1),
            y = [bs_model.call_price()] * len(price),
            name = "Black Scholes Model",
            line={'dash': 'dot'}
        )

        trace_binomial = go.Scatter(
            x = np.arange(1, 101, 1),
            y = price,
            name = "Binomial Model"
        )

        data = [trace_bs, trace_binomial]
        return {
            'data': data,
            'layout': go.Layout(
                xaxis={'title': 'N period'},
                yaxis={'title': 'Call price'},
                title='Call price (European): Black Scholes Model vs Binomial Model'
            )
        }
    elif tab == 'binomial_put':
        price = []
        for i in np.arange(1, 101, 1):
            binomial_model = Binomial_model(s, k, vol, r, T, i)
            price.append(binomial_model.put_price())
        
        trace_bs = go.Scatter(
            x = np.arange(1, 101, 1),
            y = [bs_model.put_price()] * len(price),
            name = "Black Scholes Model",
            line={'dash': 'dot'}
        )

        trace_binomial = go.Scatter(
            x = np.arange(1, 101, 1),
            y = price,
            name = "Binomial Model"
        )

        data = [trace_bs, trace_binomial]
        return {
            'data': data,
            'layout': go.Layout(
                xaxis={'title': 'N period'},
                yaxis={'title': 'Put price'},
                title='Put price (European): Black Scholes Model vs Binomial Model'
            )
        }

# app.css.append_css({'external_url': 'https://codepen.io/plotly/pen/EQZeaW.css'})
if __name__ == '__main__':
    application.run(debug=True)