# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import pymssql
from config import database
from config import table
from config import username
from config import password
from config import server

def createFig():
    conn = pymssql.connect(server,username, password,database)
    cursor = conn.cursor()
    query = f"SELECT * FROM {table}"
    df = pd.read_sql(query, conn)
    df2 = df[["BloodPressure","BMI"]]

    #fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
    fig = px.scatter(df2, x="BMI", y="BloodPressure", title='BMI Versus Blood Pressure')
    return fig






app = dash.Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='BMI-vs-Blood-pressure',
        figure=createFig()
    ),
    dcc.Interval(
        id='interval-component',
        interval=5*1000, # in milliseconds
        n_intervals=0
    )

])


@app.callback(Output('BMI-vs-Blood-pressure', 'figure'),
              Input('interval-component', 'n_intervals'))
def UpdateData(n):
    conn = pymssql.connect(server,username, password,database)
    cursor = conn.cursor()
    query = f"SELECT * FROM {table}"
    df = pd.read_sql(query, conn)
    df2 = df[["BloodPressure","BMI"]]
    fig = px.scatter(df2, x="BMI", y="BloodPressure", title='BMI Versus Blood Pressure')
    return fig




if __name__ == '__main__':
    app.run_server(debug=True)
