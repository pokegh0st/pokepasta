import os
from dotenv import load_dotenv
from datetime import datetime
from secrets import token_urlsafe
from flask import Flask, render_template, request, redirect, abort
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient
import pytz
import twowish_util
import base64

app = Flask(__name__)
load_dotenv()

DB_SECRET_KEY = os.getenv('DB_SECRET_KEY')


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        client = FaunaClient(secret=DB_SECRET_KEY)
        title = request.form.get("title").strip()
        paste_text = request.form.get("paste-text").strip()
        identifier = token_urlsafe(5)
        paste = client.query(q.create(q.collection("pastas"), {
            "data": {
                "pasta_id": identifier,
                "pasta_text": base64.b64encode(twowish_util.encrypt(paste_text)).decode("ascii"),
                "title": base64.b64encode(twowish_util.encrypt(title)).decode("ascii"),
                "date": datetime.now(pytz.UTC)
            }
        }))
        return redirect(request.host_url + identifier)
    return render_template("index.html", utc_dt=datetime.utcnow().strftime("%b %d %Y %H:%M:%S UTC"))


@app.route("/<string:pasta_id>/")
def pasta(pasta_id):
    client = FaunaClient(secret=DB_SECRET_KEY)
    try:
        pasta = client.query(q.get(q.match(q.index("pasta_index"), pasta_id)))
    except:
        abort(404)

    data = pasta["data"]
    plaintext = twowish_util.decrypt(
        base64.b64decode(data["pasta_text"].encode("ascii")))
    plaintitle = twowish_util.decrypt(
        base64.b64decode(data["title"].encode("ascii")))
    data["pasta_text"] = str(plaintext, 'utf-8')
    data["title"] = str(plaintitle, 'utf-8')

    return render_template("paste.html", pasta=data)


if __name__ == "__main__":
    app.run(debug=True)
