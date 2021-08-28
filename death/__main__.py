""" For production, instead use `gunicorn death:server` """

from . import app

app.run_server(debug=True)
