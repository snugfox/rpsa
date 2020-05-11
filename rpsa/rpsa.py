from argparse import ArgumentParser
import flask
from datetime import datetime
from threading import Lock, Timer, Thread
from pathlib import Path
from urllib import parse

from api import RPSA

APP_NAME = "rpsa"


app = flask.Flask(APP_NAME)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def index(path: str):
    if app.config["webui_addr"] != "":
        webui_addr = app.config["webui_addr"]
        webui_query = parse.urlencode({"api_origin": flask.request.host_url})
        return flask.redirect(f"{webui_addr}?{webui_query}")
    print(">", path)
    if path == "":
        path = "index.html"
    return flask.send_from_directory(str(Path(__file__).parent.joinpath("webui")), path)


@app.route("/api/candidates")
def candidates():
    api = app.config["api"]
    res = flask.jsonify(api.candidates())
    if app.config["webui_addr"] != "":
        res.headers.add("Access-Control-Allow-Origin", "*")
    return res


@app.route("/api/sentiment")
def sentiment():
    api = app.config["api"]
    res = flask.jsonify(api.sentiment())
    if app.config["webui_addr"] != "":
        res.headers.add("Access-Control-Allow-Origin", "*")
    return res


@app.route("/api/terms")
def terms():
    api = app.config["api"]
    res = flask.jsonify(api.terms())
    if app.config["webui_addr"] != "":
        res.headers.add("Access-Control-Allow-Origin", "*")
    return res


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--dev", default=False, action="store_true")
    parser.add_argument("--model", type=str, required=True)
    parser.add_argument("--webui-addr", type=str, default="")
    parser.add_argument("--sample-size", type=int, default=100)
    parser.add_argument("--candidate", type=str, required=True, action="append")
    parser.add_argument("--interval", type=int, default=60)
    args = parser.parse_args()

    api = RPSA(args.candidate, sample_size=args.sample_size, model_filename=args.model)
    Thread(target=lambda: api.run(float(args.interval)), daemon=True).start()

    app.config.update({"webui_addr": args.webui_addr, "api": api})
    if args.dev:
        app.run(debug=args.dev)
    else:
        from gevent.pywsgi import WSGIServer
        server = WSGIServer(("", 5000), app)
        server.serve_forever()
