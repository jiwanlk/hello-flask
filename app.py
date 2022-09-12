import datetime
import json
from flask import Flask, request, make_response, render_template, redirect
from redis import Redis
from rq import Queue, job
from worker import count_words_at_url
from logger import logger

app = Flask(__name__)
r = Redis(host="redis")
queue = Queue(connection=r)


@app.route("/")
def index():
    logger.debug("A new user visited our site!")
    urls_raw = request.cookies.get("urls_in_queue", "[]")
    urls = json.loads(urls_raw)
    return render_template("index.html", urls=urls)


@app.route("/add_to_queue")
@logger.catch
def add_to_queue():
    if "url" in request.args:
        url = request.args.get("url")
        if not url[:8].startswith(("https://", "http://")):
            url = "http://" + url
        urls_raw = request.cookies.get("urls_in_queue", "[]")
        urls = json.loads(urls_raw)
        job = queue.enqueue(count_words_at_url, url, result_ttl=60)
        urls = [*urls, {url: job.id}]
        url_json = json.dumps(urls)
        res = make_response(redirect("/"))
        res.set_cookie(
            "urls_in_queue",
            url_json,
            expires=datetime.datetime.now() + datetime.timedelta(minutes=1),
        )
        return res


@app.route("/results/<job_key>", methods=["GET"])
def get_results(job_key):
    if not job.Job.exists(job_key, connection=r):
        return "No job", 400
    j = job.Job.fetch(job_key, connection=r)
    if j.is_finished:
        logger.log("WORKER", "Returned Completed Job Status!")
        return str(j.result), 200
    else:
        return "No result", 202


if __name__ == "__main__":
    app.run()
