""" For production, instead use `gunicorn death.app:server` """

from .app import app

app.run_server(debug=True)
