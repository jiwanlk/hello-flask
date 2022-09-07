import os
from flask import Flask
import redis

redis_url = os.getenv("REDISTOGO_URL", "redis://redis:6379")

rdb = redis.from_url(redis_url)
if not rdb.exists("counter"):
    rdb.set("counter", 0)

app = Flask(__name__)


@app.route("/")
def index():
    rdb.incr("counter", 1)
    return f"<h1>This page has been visited {rdb.get('counter').decode()} times!</h1>"


if __name__ == "__main__":
    app.run(debug=True)
