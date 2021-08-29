## Användning

Installera miljö:

    apt install redis-server
    pip install gunicorn
    redis-server &
    export REDIS_URL=redis://localhost:6379

Hämta data regelbundet:

    ./download_data.sh
    python -m death.update

Starta webserver:

    gunicorn death.app:server
