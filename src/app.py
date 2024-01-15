import dataprep.prepare
import draw.present

from dash import Dash, dcc, html
import logging
from flask import Flask

logging.basicConfig(level=logging.INFO)

flask_app = Flask(__name__)

dash_app = Dash(server=flask_app)
dash_app.layout = html.Div([
    dcc.Graph(figure=draw.present.fig())
])

if __name__ == '__main__':
 # dash_app.run_server(debug=True, host="0.0.0.0", port=8050, use_reloader=False)
 dash_app.run_server(debug=False)
