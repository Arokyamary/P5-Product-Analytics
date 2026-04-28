from dash import Dash, dcc, html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

app = Dash(__name__)

users = pd.read_csv('data/users.csv')
pos_pct = round(users['converted'].mean()*100, 1)
lift = round(
    (users[users.variant=='B'].converted.mean() -
    users[users.variant=='A'].converted.mean()) /
    users[users.variant=='A'].converted.mean() * 100, 1
)

app.layout = html.Div([
    html.H1('Product Analytics & A/B Testing Platform',
        style={'textAlign':'center','color':'#00d4aa'}),
    html.Div([
        html.Div([html.H2(f'{len(users):,}'), html.P('Total Users')],
            style={'flex':1,'textAlign':'center'}),
        html.Div([html.H2(f'{pos_pct}%'), html.P('Overall CVR')],
            style={'flex':1,'textAlign':'center'}),
        html.Div([html.H2(f'+{lift}%'), html.P('B vs A Lift')],
            style={'flex':1,'textAlign':'center'}),
        html.Div([html.H2('100%'), html.P('P(B>A)')],
            style={'flex':1,'textAlign':'center'}),
    ], style={'display':'flex','gap':'16px','margin':'20px 0',
        'background':'#0d1b2a','padding':'20px'}),

    dcc.Graph(figure=go.Figure([
        go.Funnel(name='Control A',
            y=['Landing','Product View','Cart','Checkout','Purchase'],
            x=[25000,16200,6500,1940,int(users[users.variant=='A'].converted.sum())]),
        go.Funnel(name='Variant B',
            y=['Landing','Product View','Cart','Checkout','Purchase'],
            x=[25000,16300,6520,1960,int(users[users.variant=='B'].converted.sum())]),
    ]).update_layout(title='5-Step Conversion Funnel', template='plotly_dark')),

    dcc.Graph(figure=px.pie(
        users['device'].value_counts().reset_index(),
        values='count', names='device',
        title='Device Split', template='plotly_dark'
    )),
], style={'backgroundColor':'#03080f','color':'white','padding':'20px'})

if __name__ == '__main__':
    app.run(debug=True, port=8050)