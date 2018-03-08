import time
import datetime
import requests
import sqlite3
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd


app = dash.Dash(__name__)
app.layout = html.Div(
    html.Div([
        html.H1('Crypto Dashboard'),
	html.Div(id='live-update-text'),
	html.Div(id='live-update-text1'),
        dcc.Graph(id='live-update-graph'),
	dcc.Graph(id='word-bubble'),
	html.H3('Richard Anderson'),
	html.H3('Krista Bennatti'),
	html.H3('Sabrina Mancini'),	
	html.H3('Rubaiya Islam'),
	html.H3('Kofi Wang'),
        dcc.Interval(
            id='interval-component',
            interval=10*1000, # in milliseconds
            n_intervals=0
        )
    ])
)


@app.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    conn = sqlite3.connect('crypto.db')
    c = conn.cursor()
    cur = pd.read_sql_query('SELECT price FROM current_data',conn)
    price= cur.iloc[0]['price']
    style = {'padding': '5px', 'fontSize': '28px'}
    return [
        #html.Span('time: {0:.2f}'.format(time), style=style),
        html.Span('Bitcoin Price: {0:.2f}'.format(price), style=style),
    ]
    conn.close()

@app.callback(Output('live-update-text1', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics1(n):
    conn = sqlite3.connect('crypto.db')
    c = conn.cursor()
    cla = pd.read_sql_query('SELECT title FROM sentiment',conn)
    pre= str(cla.iloc[0]['title'])
    style = {'padding': '5px', 'fontSize': '28px'}
    return [
        #html.Span('time: {0:.2f}'.format(time), style=style),
        html.Span(format(pre), style=style),
    ]
    conn.close()

# Multiple components can update every/home/kofi/Data Science II/project_a/ccn_words_bubble.pytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    conn = sqlite3.connect('crypto.db')
    c = conn.cursor()
    his = pd.read_sql_query('SELECT * FROM historical_data',conn)
    tweet = pd.read_sql_query('SELECT * FROM all_tags',conn)
    data = {
        'time_1': tweet['time'],
        'btc': tweet['bitcoin'],
	'eth': tweet['ethereum'],    
        'time_2': his['time'],
        'price': his['price'],
    }
    conn.close()
    # Create the graph with subplots
    fig = plotly.tools.make_subplots(rows=2, cols=1, vertical_spacing=0.2)
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}
    
    trace1 = go.Scatter(x=data['time_1'], y=data['btc'], mode='lines', name='BTC tweets', showlegend=True)
    trace2 = go.Scatter(x=data['time_1'], y=data['eth'], mode='lines', name='ETH tweets', showlegend=True)
    fig.append_trace({
        'x': data['time_2'],
        'y': data['price'],
	'name':'BTC price',
     }, 1,1)
    fig.append_trace(trace1, 2, 1)
    fig.append_trace(trace2, 2, 1)
    return fig

@app.callback(Output('word-bubble', 'figure'),
	      [Input('interval-component', 'n_intervals')])
def word_bubble(n):
    conn = sqlite3.connect('crypto.db')
    c = conn.cursor()
    words = pd.read_sql_query('SELECT * FROM sortedTFIDF LIMIT 20',conn)
    conn.close()
    topVal = words['value']
    topKey = words['word']
    x = []
    z =[10,10,10,5,15,5,15,5,15,7.2,12.7,7.2,2.5,17.5,17.5,12.5,12.5,7.5,12.5,7.5]    
    for i in range(len(z)):
        x.append(z[i])
    y = [10,16,4,10,10,5,5,15,15,2.5,2.5,17.5,11.8,12.5,7.5,12.5,18,8,8,12.5]

   
    color=[2.8621445978503819,
 2.5961561323897606,
 2.4182501728584671,
 1.6585707333299744,
 1.5101018434894153,
 0.90411573108679022,
 0.89219043260259112,
 0.83214353859979939,
 0.70678014123161492,
 0.67268923294671967,
 0.52985445641963635,
 0.4334247552913475,
 -0.098212315427697289,
 -0.32654536888436603,
 -0.42722404855653329,
 -0.53011315178865592,
 -0.57035499653017185,
 -0.67214927099168442,
 -0.8572816821147381,
 -1.1882035639201587]
    trace1 = go.Scatter(
        x=x,
        y=y,
        text=topKey,
        mode='markers+text',
        marker=dict(color=color, size=1.5*topVal, sizemode='area', sizeref=2.*max(topVal)/(250.**2)))
    
    layout=go.Layout(
	height=1500,
	width=1500,
	title='Today\'s Top 20 Words Based on TF-IDF', 
        titlefont=dict(size=32),    
	xaxis=dict(
            title='Source: Crypto Coins News (www.ccn.com) API: https://newsapi.org/v2/everything?sources=crypto-coins-news&apiKey=1d656ac0916147bf8d28e1dcda71266a',
            autorange=True,
            showgrid=False,
            zeroline=False,
            showline=False,
            autotick=True,
            ticks='',
            showticklabels=False
        ),
        yaxis=dict(
            autorange=True,
            showgrid=False,
            zeroline=False,
            showline=False,
            autotick=True,
            ticks='',
            showticklabels=False

        ),
	orientation=270
	#margin=go.Margin(t=45, l=50, r=50)
    )
    #fig = plotly.tools.make_subplots(rows=1, cols=1, vertical_spacing=0.2)
    #fig['layout']=layout
    #fig.append_trace(trace1, layout, 1,1)
    
    fig = go.Figure(data=[trace1], layout=layout)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

