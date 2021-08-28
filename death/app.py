from os import environ
from io import BytesIO

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
from flask_caching import Cache

cache = Cache(
    config={
        "CACHE_TYPE": "RedisCache",
        "CACHE_KEY_PREFIX": "",
        "CACHE_REDIS_URL": environ.get("REDIS_URL"),
    }
)

app = dash.Dash(__name__)
server = app.server
cache.init_app(server)


def serve_layout():
    data = {
        "yearly": {
            "df": pd.read_pickle(BytesIO(cache.get("yearly"))),
            "mode": "markers",
            "name": "Årlig statistik sedan 1749",
        },
        "monthly": {
            "df": pd.read_pickle(BytesIO(cache.get("monthly"))),
            "mode": "lines",
            "name": "Månatlig statistik sedan 2000",
        },
        "recent": {
            "df": pd.read_pickle(BytesIO(cache.get("recent"))),
            "mode": "lines",
            "name": "Månatlig preliminär statistik",
        },
    }

    fig = go.Figure()

    for d in data.values():
        fig.add_scatter(x=d["df"].index, y=d["df"], name=d["name"], mode=d["mode"])

    fig.layout.yaxis.tickformat = ",.2%"
    fig.layout.title = "Andel av befolkningen som dött under ett år"
    fig.layout.xaxis.title = "Året som löpte fram till datum"
    fig.layout.yaxis.title = "Andel som dött"
    fig.layout.yaxis.rangemode = "tozero"

    return html.Div(
        [
            dcc.Markdown(
                """
                # Döda i Sverige
                """
            ),
            dcc.Graph(id="graph", figure=fig),
            dcc.Markdown(
                """
                Källor:

                * https://www.scb.se/hitta-statistik/statistik-efter-amne/befolkning/befolkningens-sammansattning/befolkningsstatistik/pong/tabell-och-diagram/preliminar-statistik-over-doda/
                * http://api.scb.se/OV0104/v1/doris/sv/ssd/START/BE/BE0101/BE0101G/BefUtvKon1749
                * http://api.scb.se/OV0104/v1/doris/sv/ssd/START/BE/BE0101/BE0101G/ManadBefStatRegion
                """
            ),
        ]
    )


app.layout = serve_layout  # Called every user page refresh
