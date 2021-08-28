# -*- coding: utf-8 -*-

# Run this app with `python -m app` and
# visit http://127.0.0.1:8050/ in your web browser.

"""Andel av befolkningen som dött under ett år"""

__version__ = '0.1.0'


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from . import scb
from . import prel

app = dash.Dash(__name__)

data = {
    "yearly": {
        "df": scb.load_yearly(),
        "mode": "markers",
        "name": "Årlig statistik sedan 1749",
    },
    "monthly": {
        "df": scb.load_monthly(),
        "mode": "lines",
        "name": "Månatlig statistik sedan 2000",
    },
    "recent": {
        "df": prel.load(),
        "mode": "lines",
        "name": "Månatlig preliminär statistik",
    },
}

fig = go.Figure()

for tag, d in data.items():
    fig.add_scatter(x=d["df"].index, y=d["df"], name=d["name"], mode=d["mode"])

fig.layout.yaxis.tickformat = ",.2%"
fig.layout.title = "Andel av befolkningen som dött under ett år"
fig.layout.xaxis.title = "Året som löpte fram till datum"
fig.layout.yaxis.title = "Andel som dött"
fig.layout.yaxis.rangemode = "tozero"

app.layout = html.Div(
    [
        dcc.Markdown(
            """
            # Döda i Sverige
            """
        ),
        dcc.Graph(id="example-graph", figure=fig),
        dcc.Markdown(
            """
            Källor:

                mkdir -p data

                curl https://www.scb.se/hitta-statistik/statistik-efter-amne/befolkning/befolkningens-sammansattning/befolkningsstatistik/pong/tabell-och-diagram/preliminar-statistik-over-doda/ -o data/prel.xlsx -L
                curl http://api.scb.se/OV0104/v1/doris/sv/ssd/START/BE/BE0101/BE0101G/BefUtvKon1749 -H "Content-Type: application/json" -d @scb_queries/BefUtvKon1749.json | json_pp --json_opt utf8,pretty > data/BefUtvKon1749.json
                curl http://api.scb.se/OV0104/v1/doris/sv/ssd/START/BE/BE0101/BE0101G/ManadBefStatRegion -H "Content-Type: application/json" -d @scb_queries/ManadBefStatRegion.json | json_pp --json_opt utf8,pretty > data/ManadBefStatRegion.json

            """
        ),
    ]
)

server = app.server
