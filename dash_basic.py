# Run this app with:
#  >conda activate base
#  >pip install dash (if not done previously)
#  >python dash_basic.py
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# for later iterations:
# import pymssql
# from config import database
# from config import table
# from config import username
# from config import password
# from config import server

app = dash.Dash(__name__)

df = pd.read_csv('data/Cars93.csv')

df2 = df[['Weight', 'MPG.city', 'MPG.highway']]

fig = px.scatter(df2, x='Weight', y='MPG.city', title='MPG (city) vs Weight')
fig2 = px.scatter(df2, x='Weight', y='MPG.highway', title='MPG (highway) vs Weight')

app.layout = html.Div(children=[
    html.H1(children='Hello Dash!'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='first-graph',
        figure=fig
    ),

    dcc.Graph(
            id='example-graph',
            figure=fig2
    )
])


if __name__ == '__main__':
    app.run_server()
