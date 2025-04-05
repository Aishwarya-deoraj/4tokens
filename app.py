from flask import Flask, jsonify, render_template
import pandas as pd

app = Flask(__name__)
df = pd.read_csv("data/dummy.csv")

@app.route("/")
def dashboard():
    return render_template("dashboard.html", title="Feature Tracker Dashboard")

@app.route("/features")
def show_features():
    df_html = df.to_html(classes="table table-hover table-bordered table-striped", index=False)
    return render_template("table.html", title="All Feature Requests", table=df_html)


@app.route("/priority")
def next_priority():
    top_features = df.head(3).to_dict(orient='records')  # Get top 3 rows as dicts
    return render_template("priority.html", title="Next Priority Feature", features=top_features)

@app.route("/idea/<string:id>")  # Changed from <int:id> to <string:id>
def get_idea(id):
    # Filter dataframe by UUID string match
    idea = df[df['ID'] == id]
    if not idea.empty:
        return render_template("view_idea.html", idea=idea.iloc[0])
    else:
        return jsonify({"error": "Idea not found"}), 404
