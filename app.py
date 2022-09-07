from flask import Flask, request
from redis import Redis
from rq import Queue
from worker import count_words_at_url

app = Flask(__name__)
queue = Queue(connection=Redis(host="redis"))


@app.route("/")
def index():
    if "url" in request.args:
        queue.enqueue(count_words_at_url, request.args.get("url"))
    return "Counting going on..."


if __name__ == "__main__":
    app.run(debug=True)
