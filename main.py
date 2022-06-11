from flask import Flask, render_template, redirect, url_for, flash, jsonify
from flask_bootstrap import Bootstrap
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_gravatar import Gravatar
import os
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
Bootstrap(app)
gravatar = Gravatar(app, size=100, rating='g', default='retro', force_default=False, force_lower=False, use_ssl=False, base_url=None)

df = pd.read_csv("whole_yandex.csv")
data = []
for ind, dat in df.iterrows():
    data.append({"url": dat["url"].strip(), "status": int(dat["status"]), "id": ind})


@app.route('/')
def get_all_data():
    return render_template("index.html", all_data=data)


@app.route("/status_true/<int:dat_id>", methods=["GET", "POST"])
def status_one(dat_id):
    data[dat_id]["status"] = 1
    pd.DataFrame(data).to_csv("whole_yandex.csv", index=False)
    return redirect("/processed")


@app.route("/status_false/<int:dat_id>", methods=["GET", "POST"])
def status_minus_one(dat_id):
    data[dat_id]["status"] = -1
    pd.DataFrame(data).to_csv("whole_yandex.csv", index=False)
    return redirect("/unprocessed")


@app.route('/processed')
def get_processed():
    processed = [i for i in data if i["status"] == 1]
    return render_template("index.html", all_data=processed)


@app.route('/unprocessed')
def get_unprocessed():
    unprocessed = [i for i in data if i["status"] == -1]
    return render_template("index.html", all_data=unprocessed)


@app.route('/inprogress')
def get_inprogress():
    unprocessed = [i for i in data if i["status"] == 0]
    return render_template("index.html", all_data=unprocessed)


if __name__ == "__main__":
    app.run(debug=True)
