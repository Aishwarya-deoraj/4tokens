from flask import Flask, jsonify, render_template
import pandas as pd

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
    # Send top 3 ideas to the priority template
    top_features = df.head(3).to_dict(orient='records')
    return render_template("priority.html", title="Next Priority Feature", features=top_features)

@app.route("/idea/<string:id>") 
def get_idea(id):
    # Show individual idea detail page
    idea = df[df['ID'] == id]
    if not idea.empty:
        return render_template("view_idea.html", idea=idea.iloc[0])
    else:
        return jsonify({"error": "Idea not found"}), 404