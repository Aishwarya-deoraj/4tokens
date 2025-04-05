
from flask import Flask, jsonify, render_template
import ast
import pandas as pd
from data import id_to_comments, dependencies_projects_ids, supports_project_ids

app = Flask(__name__)
df = pd.read_csv("data/dummy_2.csv")

@app.route('/')
def index():
    # Only the columns we want to show in the table
    df_filtered = df[['Title', 'Description', 'Upvotes', 'Submission Date', 'Status']]

    # Store Title → ID mapping to use for client-side redirection
    title_to_id = df.set_index('Title')['ID'].to_dict()

    # Render table
    table_html = df_filtered.to_html(classes='table table-striped', index=False, table_id="myTable")

    return render_template("table.html", title="All Feature Requests", table=table_html, title_to_id=title_to_id)


@app.route("/priority")
def next_priority():
    top_features = df.head(3).to_dict(orient='records')
    top_ids = df.head(3)['ID'].tolist()

    def get_support_list(feature_id):
        ids = supports_project_ids.get(feature_id, [])
        return [{"id": sid, "title": df[df['ID'] == sid]['Title'].values[0] if not df[df['ID'] == sid].empty else sid} for sid in ids]

    supp1 = get_support_list(top_ids[0])
    supp2 = get_support_list(top_ids[1])
    supp3 = get_support_list(top_ids[2])

    return render_template(
        "priority.html",
        title="Next Priority Feature",
        features=top_features,
        supp1=supp1,
        supp2=supp2,
        supp3=supp3
    )


@app.route("/idea/<string:id>")
def get_idea(id):
    idea = df[df['ID'] == id]
    if not idea.empty:
        # Safe comment handling
        comment_str = id_to_comments.get(id, "[]")
        comments = ast.literal_eval(comment_str) if isinstance(comment_str, str) else comment_str

        # Safe dependency handling
        dep_str = dependencies_projects_ids.get(id, [])
        dep_ids = ast.literal_eval(dep_str) if isinstance(dep_str, str) else dep_str

        dep_titles = {}
        for dep_id in dep_ids:
            match = df[df['ID'] == dep_id]
            dep_titles[dep_id] = match['Title'].values[0] if not match.empty else dep_id

        return render_template(
            "view_idea.html",
            idea=idea.iloc[0],
            comments=comments,
            dependencies=dep_ids,
            dep_titles=dep_titles
        )
    else:
        return jsonify({"error": "Idea not found"}), 404