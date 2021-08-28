from os import environ
from io import BytesIO

import redis

from . import scb
from . import prel


cache = redis.from_url(environ.get("REDIS_URL"))

data = {
    "yearly": scb.load_yearly(),
    "monthly": scb.load_monthly(),
    "recent": prel.load(),
}

for k, v in data.items():
    with BytesIO() as f:
        v.to_pickle(f)
        cache.set(k, f.getvalue())
