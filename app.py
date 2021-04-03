
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
from dash.exceptions import PreventUpdate





app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.config['suppress_callback_exceptions'] = True
app.config.suppress_callback_exceptions = True

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

server = app.server