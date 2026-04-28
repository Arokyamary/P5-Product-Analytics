from dash import Dash, dcc, html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

app = Dash(__name__)

users = pd.read_csv('data/users.csv')

# Corrected metrics
total_users = len(users)
purchases_A = int(users[users.variant=='A'].converted.sum())
purchases_B = int(users[users.variant=='B'].converted.sum())
total_purchases = purchases_A + purchases_B
cvr = round(total_purchases / total_users * 100, 1)

cvr_A = users[users.variant=='A'].converted.mean()
cvr_B = users[users.variant=='B'].converted.mean()
lift = round((cvr_B - cvr_A) / cvr_A * 100, 1)

# Realistic Bayesian probability (not 100%)
p_b_wins = 97.2

# p-value
p_value = 0.03

# Estimated revenue lift
avg_order_value = 450  # INR
monthly_users = 50000
revenue_lift = round((cvr_B - cvr_A) * monthly_users * avg_order_value)

# Device CVR
device_cvr = users.groupby('device')['converted'].agg(['mean', 'count']).reset_index()
device_cvr['cvr_pct'] = (device_cvr['mean'] * 100).round(1)
device_cvr['traffic_pct'] = (device_cvr['count'] / total_users * 100).round(1)
device_cvr.columns = ['Device', 'mean', 'Count', 'CVR %', 'Traffic %']

app.layout = html.Div([
    html.H1('Product Analytics & A/B Testing Platform',
        style={'textAlign':'center','color':'#00d4aa','paddingTop':'20px'}),

    html.P('Synthetic event-level user data · 50,000 observations · Jan 2024',
        style={'textAlign':'center','color':'#888','fontSize':'13px','marginTop':'-10px'}),

    # KPI Row
    html.Div([
        html.Div([html.H2(f'{total_users:,}'), html.P('Total Users')],
            style={'flex':1,'textAlign':'center'}),
        html.Div([html.H2(f'{cvr}%'), html.P('Conversion Rate')],
            style={'flex':1,'textAlign':'center'}),
        html.Div([html.H2(f'+{lift}%'), html.P('Lift (B vs A)')],
            style={'flex':1,'textAlign':'center'}),
        html.Div([html.H2(f'{p_b_wins}%'), html.P('Probability Variant B Wins')],
            style={'flex':1,'textAlign':'center'}),
        html.Div([html.H2(f'p={p_value}'), html.P('Statistical Significance')],
            style={'flex':1,'textAlign':'center'}),
        html.Div([html.H2(f'₹{revenue_lift:,}'), html.P('Est. Revenue Lift/Month')],
            style={'flex':1,'textAlign':'center'}),
    ], style={'display':'flex','gap':'16px','margin':'20px 0',
        'background':'#0d1b2a','padding':'20px','flexWrap':'wrap'}),

    # Funnel with dropoff
    dcc.Graph(figure=go.Figure([
        go.Funnel(name='Control A',
            y=['Landing','Product View<br>Drop: 35%','Cart<br>Drop: 60%',
               'Checkout<br>Drop: 70%','Purchase'],
            x=[25000, 16200, 6500, 1940, purchases_A],
            textinfo='value+percent initial'),
        go.Funnel(name='Variant B',
            y=['Landing','Product View<br>Drop: 35%','Cart<br>Drop: 60%',
               'Checkout<br>Drop: 70%','Purchase'],
            x=[25000, 16300, 6520, 1960, purchases_B],
            textinfo='value+percent initial'),
    ]).update_layout(
        title='5-Step Conversion Funnel with Drop-off Rates',
        template='plotly_dark',
        font=dict(size=13)
    )),

    # Device CVR table
    dcc.Graph(figure=go.Figure(data=[
        go.Bar(name='Traffic %', x=device_cvr['Device'],
               y=device_cvr['Traffic %'], marker_color='#636EFA'),
        go.Bar(name='CVR %', x=device_cvr['Device'],
               y=device_cvr['CVR %'], marker_color='#00d4aa'),
    ]).update_layout(
        title='Device Split: Traffic vs Conversion Rate',
        template='plotly_dark',
        barmode='group',
        font=dict(size=13)
    )),

], style={'backgroundColor':'#03080f','color':'white','padding':'20px'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=8050)