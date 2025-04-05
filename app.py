from flask import Flask, jsonify, render_template
import pandas as pd
from data import id_to_comments, dependencies, supports

app = Flask(__name__)
df = pd.read_csv("data/dummy_2.csv")

@app.route("/")
def show_ideas():
    df_html = df.to_html(
        classes="table table-hover table-bordered table-striped",
        index=False,
        table_id="myTable" 
    )
    return render_template("table.html", title="All Feature Requests", table=df_html)


@app.route("/priority")
def next_priority():
    top_features = df.head(3).to_dict(orient='records')
    top_ids = df.head(3)['ID'].tolist()
    return render_template("priority.html", title="Next Priority Feature", features=top_features, supp1=supports[top_ids[0]],supp2=supports[top_ids[1]],supp3=supports[top_ids[2]])

@app.route("/idea/<string:id>") 
def get_idea(id):
    idea = df[df['ID'] == id]
    if not idea.empty:
        return render_template("view_idea.html", idea=idea.iloc[0],comments=id_to_comments[id],dependencies=dependencies[id])
    else:
        return jsonify({"error": "Idea not found"}), 404