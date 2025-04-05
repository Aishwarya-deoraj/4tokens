from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route("/")
def dashboard():
    return render_template("dashboard.html", title="Feature Tracker Dashboard")

@app.route("/features")
def show_features():
    df = pd.read_csv("data/dummy.csv")
    df_html = df.to_html(classes="table table-hover table-bordered table-striped", index=False)
    return render_template("table.html", title="All Feature Requests", table=df_html)


@app.route("/priority")
def next_priority():
    return render_template("priority.html", title="Next Priority Feature")
