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

app = dash.Dash(
    __name__,
    title="Döda i Sverige",
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

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

    fig.update_layout(
        {
            "title": "Andel av befolkningen som dött under ett år",
            "yaxis": {
                "title": "Andel som dött",
                "tickformat": ",.2%",
                "rangemode": "tozero",
            },
            "xaxis": {"title": "Året som löpte fram till datum"},
            "legend": {"yanchor": "top", "y": 0.99, "xanchor": "left", "x": 0.01},
            "margin": {"l": 10, "r": 10, "t": 80, "b": 10},
        }
    )

    return html.Div(
        [
            dcc.Markdown(
                """
                # Döda i Sverige
                """
            ),
            dcc.Graph(id="graph", figure=fig, responsive=True),
            dcc.Markdown(
                f"""
                Källor:

                * [SCB: Befolkningsutvecklingen i riket efter kön](http://api.scb.se/OV0104/v1/doris/sv/ssd/START/BE/BE0101/BE0101G/BefUtvKon1749)
                * [SCB: Befolkningsstatistik efter region och kön](http://api.scb.se/OV0104/v1/doris/sv/ssd/START/BE/BE0101/BE0101G/ManadBefStatRegion)
                * [SCB: Preliminär statistik över döda]({cache.get("prel-url").decode("utf8")})

                [Källkod](https://github.com/per42/death/tree/master)
                """
            ),
        ]
    )


app.layout = serve_layout  # Called every user page refresh
