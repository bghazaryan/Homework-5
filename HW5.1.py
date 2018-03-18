import dash
import quandl
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from plotly.offline import plot
import plotly.graph_objs as go


import plotly.graph_objs as go

import churn_p
import startup_chart_p

import BC_GO_box_p
import BC_GO_table_p


Homework_title = html.H1(children="Homework 5", style={'color': 'brown', 'text-align':'center', 'font-family': 'Comic Sans MS'})

app = dash.Dash()
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

# Assignment 1

churn_graph = dcc.Graph(id="churn_p", figure=churn_p.figure_churn)
startup_chart = dcc.Graph(id="startup_chart_p", figure=startup_chart_p.startup_chart)


Churn_graph_title = html.H3(children="Employee churn")
Statrup_graph_title = html.H3(children="Startup Roadmap")

Churn_graph = html.Div([
    churn_graph],
    className='eight columns'
    )
Startup_graph = html.Div([
    startup_chart],
    className='eight columns'
    )


Assignment_1 = html.Div([html.Div([
    dcc.RadioItems(
        id = 'ass1_radio_in',
        options=[
            {'label': 'Employee churn', 'value': 1},
            {'label': 'Startup Roadmap', 'value': 2},
        ]
        #value=1)],className='two columns'),
        )],className='two columns'),
    html.Div([], id='ass1_out')
    ], className='row')


# Assignment 2

quandl.ApiConfig.api_key = "HyaKYY8tnWQAgPyX36rL"

apple_data = quandl.get("WIKI/AAPL")
google_data = quandl.get("WIKI/GOOGL")
fb_data = quandl.get("WIKI/FB")
amazon_data = quandl.get("WIKI/AMZN")
microsoft_data = quandl.get("BCHARTS/ABUCOINSUSD")

Assignment_2 = html.Div([
    	dcc.Dropdown(
        id = 'ass2_dd_in',
        className = 'two columns',
        options=[   
            {'label': 'Apple',     'value': 'AAPL'},
            {'label': 'Google',    'value': 'GOOGL'},
            {'label': 'Facebook',  'value': 'FB'},
            {'label': 'Amazon',    'value': 'AMZN'},
            {'label': 'Bitcoin',   'value': 'BCHARTS'}
        ],
        multi=True,
        placeholder="Please, select a stock"),
    	html.Div([], id = "ass2_out", className = 'ten columns'),
    ], className='row')


# Assignment 3
gdp = quandl.get("FRED/GDP")

Assignment_3 = html.Div([
            html.Div([
                dcc.Graph(id='ass3_graph_out'),
                dcc.RangeSlider(
                id = 'ass3_in',
                min = 0,
                max = len(gdp.index),
                step = 1,
                value=[0, len(gdp.index)]),
            ])  
    ],  className='row')


# Application

container = html.Div([
    Homework_title,
	Assignment_1,
    Assignment_2,
    Assignment_3,
	], className='row')

app.layout = html.Div([container], className='row')



@app.callback(
    Output(component_id='ass1_out', component_property='children'),
    [Input(component_id='ass1_radio_in', component_property='value')]
)
def update_1(input_value):
    if (input_value == 1):
        return Churn_graph
    elif (input_value == 2):
        return Startup_graph
    else:
        return html.H2(children='Please select one graph.', style={'color': 'red', 'text-align':'center'})

@app.callback(
    Output(component_id='ass2_out', component_property='children'),
    [Input(component_id='ass2_dd_in', component_property='value')]
)
def update_2(stocks):
    if stocks and len(stocks) == 2:
        header = []
        cells  = []
        box = []
        for brand in stocks:
            if(brand=='AAPL'):
                header.append('<b>Apple</b>')
                cells.append(round(apple_data.Open.pct_change()[1:5,],3))
                box.append(go.Box(x=apple_data.Open.pct_change(), name = 'Apple'))
            elif(brand=='GOOGL'):
                header.append('<b>Google</b>')
                cells.append(round(google_data.Open.pct_change()[1:5,],3))
                box.append(go.Box(x=google_data.Open.pct_change(), name = 'Google'))
            elif(brand=='FB'):
                header.append('<b>Facebook</b>')
                cells.append(round(fb_data.Open.pct_change()[1:5,],3))
                box.append(go.Box(x=fb_data.Open.pct_change(), name = 'Facebook'))
            elif(brand=='AMZN'):
                header.append('<b>Amazon</b>')
                cells.append(round(amazon_data.Open.pct_change()[1:5,],3))
                box.append(go.Box(x=amazon_data.Open.pct_change(), name = 'Amazon'))
            elif(brand=='BCHARTS'):
                header.append('<b>Bitcoin</b>')
                cells.append(round(microsoft_data.Open.pct_change()[1:5,],3))
                box.append(go.Box(x=microsoft_data.Open.pct_change(), name = 'Bitcoin'))

        mainDiv = html.Div([buildBox(box), buildTable(header, cells)], className='ten columns' )

        return mainDiv

    else:
        return html.H2(children='Choose exactly two stocks.', style={'color': 'red', 'text-align':'center'})


def buildBox(box_data):
    box_layout = dict(title = "<i><b>Distribution of Prices</b></i>")
    box_figure = dict(data=box_data, layout=box_layout)
    box = dcc.Graph(id="box", figure=box_figure, className = 'eight columns')
    return box

def buildTable(header, cells):
	header = dict(values = header,
			    fill = dict(color='#119DFF')
             )
	cells = dict(values = cells,
			    fill = dict(color = ["yellow","white"])
            )
	trace = go.Table(header = header, cells=cells)
	data = [trace]
	layout = dict(width=300, height=300)
	figure = dict(data=data, layout=layout)
	table = dcc.Graph(id="table_it", figure=figure, className = 'two columns')
	return table

@app.callback(
    Output(component_id='ass3_graph_out', component_property='figure'),
    [Input(component_id='ass3_in', component_property='value')]
)
def update_3(input_value):
    if (input_value):
        print (input_value)
    modified_index = gdp.index[input_value[0]:input_value[1]]
    modified_values = gdp.Value[input_value[0]:input_value[1]]
    data = [go.Scatter(x=modified_index,y=modified_values,fill="tozeroy")]
    layout = dict(title = '<b>US GDP over time</b>')
    figure = dict(data=data, layout = layout)
    return figure

if __name__ == '__main__':
    app.run_server()