"""
This app creates a responsive sidebar layout with dash-bootstrap-components and
some custom css with media queries.
When the screen is small, the sidebar moved to the top of the page, and the
links get hidden in a collapse element. We use a callback to toggle the
collapse when on a small screen, and the custom CSS to hide the toggle, and
force the collapse to stay open when the screen is large.
dcc.Location is used to track the current location, a callback uses the current
location to render the appropriate page content. The active prop of each
NavLink is set automatically according to the current pathname. To use this
feature you must install dash-bootstrap-components >= 0.11.0.
For more details on building multi-page Dash applications, check out the Dash
documentation: https://dash.plot.ly/urls
"""
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html
import dash_html_components as html
import plotly.express as px
import pandas as pd
# import pymssql

from config import database
from config import table
from config import username
from config import password
from config import server

# try:
#     conn = pymssql.connect(server,username, password,database)

#     cursor = conn.cursor()
#     # select 26 rows from SQL table to insert in dataframe.
#     query = f"SELECT * FROM {table}"
#     df = pd.read_sql(query, conn)
# except Exception as e:
#     print(e)

# print(df.info())

# df2 = df[["BloodPressure","BMI"]]
# print(df2)

df = pd.read_csv('data/Cars93.csv')
df2 = df[['Weight', 'MPG.city']]
# print(df.shape)
# df2.head(3)
df3 = df[["Pregnancies","Glucose"]]



fig = px.scatter(df2, x="BMI", y="BloodPressure", title='BMI Versus Blood Pressure')
fig2 = px.scatter(df3, x="Pregnancies", y="Glucose", title='Pregancy versus Glucose')




# link fontawesome to get the chevron icons
FA = "https://use.fontawesome.com/releases/v5.8.1/css/all.css"

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, FA])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

submenu_1 = [
    html.Li(
        # use Row and Col components to position the chevrons
        dbc.Row(
            [
                dbc.Col("Set of graphs"),
                dbc.Col(
                    html.I(className="fas fa-chevron-right me-3"),
                    width="auto",
                ),
            ],
            className="my-1",
        ),
        style={"cursor": "pointer"},
        id="submenu-1",
    ),
    # we use the Collapse component to hide and reveal the navigation links
    dbc.Collapse(
        [
            dbc.NavLink("Page 1.1", href="/page-1/1"),
            dbc.NavLink("Page 1.2", href="/page-1/2"),
        ],
        id="submenu-1-collapse",
    ),
]

submenu_2 = [
    html.Li(
        dbc.Row(
            [
                dbc.Col("Menu 2"),
                dbc.Col(
                    html.I(className="fas fa-chevron-right me-3"),
                    width="auto",
                ),
            ],
            className="my-1",
        ),
        style={"cursor": "pointer"},
        id="submenu-2",
    ),
    dbc.Collapse(
        [
            dbc.NavLink("Page 2.1", href="/page-2/1"),
            dbc.NavLink("Page 2.2", href="/page-2/2"),
        ],
        id="submenu-2-collapse",
    ),
]


sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "A sidebar with collapsible navigation links", className="lead"
        ),
        dbc.Nav(submenu_1 + submenu_2, vertical=True),
    ],
    style=SIDEBAR_STYLE,
    id="sidebar",
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


# this function is used to toggle the is_open property of each Collapse
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# this function applies the "open" class to rotate the chevron
def set_navitem_class(is_open):
    if is_open:
        return "open"
    return ""


for i in [1, 2]:
    app.callback(
        Output(f"submenu-{i}-collapse", "is_open"),
        [Input(f"submenu-{i}", "n_clicks")],
        [State(f"submenu-{i}-collapse", "is_open")],
    )(toggle_collapse)

    app.callback(
        Output(f"submenu-{i}", "className"),
        [Input(f"submenu-{i}-collapse", "is_open")],
    )(set_navitem_class)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1/1"]:
        return dcc.Graph(
            id='BMI versus bloodpressure',
            figure=fig2
        ),dcc.Graph(
            id='BMI versus bloodpressure',
            figure=fig
        ),dcc.Graph(
            id='BMI versus bloodpressure',
            figure=fig
        ),dcc.Graph(
            id='BMI versus bloodpressure',
            figure=fig
        ),dcc.Graph(
            id='BMI versus bloodpressure',
            figure=fig
        )
    elif pathname == "/page-1/2":
        return dcc.Graph(
            id='BMI versus bloodpressure',
            figure=fig
        )
    elif pathname == "/page-2/1":
        return html.P("Oh cool, this is page 2.1!")
    elif pathname == "/page-2/2":
        return html.P("No way! This is page 2.2!")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == "__main__":
    app.run_server(port=8888, debug=True)