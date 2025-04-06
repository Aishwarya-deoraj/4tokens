

import base64
from flask import Flask, jsonify, render_template, request, Response
import ast
import pandas as pd
from data_maps import id_to_comments, dependencies_projects_ids, supports_project_ids
from priority_ai_agent import top3_ideas
from chain_of_thought import cot

app = Flask(__name__)
df = pd.read_csv("data/dummy_2.csv")

@app.route('/')
def index():
    df_filtered = df[['Title', 'Description', 'Upvotes', 'Submission Date', 'Status']]

    title_to_id = df.set_index('Title')['ID'].to_dict()

    table_html = df_filtered.to_html(classes='table table-striped', index=False, table_id="myTable")

    return render_template("table.html", title="All Feature Requests", table=table_html, title_to_id=title_to_id)



@app.route("/priority")
def priority_loading():
    return render_template("priority_loading.html", title="Generating Priority...")


@app.route("/priority/result", methods=["GET", "POST"])
def next_priority():
    business_impact = int(request.form.get("business_impact", 4))
    roi = int(request.form.get("roi", 3))
    strategic_impact = int(request.form.get("strategic_impact", 3))

    li = ast.literal_eval(top3_ideas(business_impact, roi, strategic_impact))

    id1, title1 = li[0]['id'], li[0]['title']
    id2, title2 = li[1]['id'], li[1]['title']
    id3, title3 = li[2]['id'], li[2]['title']

    def get_support_list(feature_id):
        ids = supports_project_ids.get(feature_id, [])
        return [
            {"id": sid, "title": df[df['ID'] == sid]['Title'].values[0] if not df[df['ID'] == sid].empty else sid}
            for sid in ids
        ]

    supp1 = get_support_list(id1)
    supp2 = get_support_list(id2)
    supp3 = get_support_list(id3)

    return render_template(
        "priority.html",
        title="Next Priority Feature",
        features=[
            {"ID": id1, "Title": title1},
            {"ID": id2, "Title": title2},
            {"ID": id3, "Title": title3}
        ],
        supp1=supp1,
        supp2=supp2,
        supp3=supp3,
        business_impact=business_impact,
        roi=roi,
        strategic_impact=strategic_impact
    )


@app.route("/idea/<string:id>")
def get_idea(id):
    tdf=pd.read_csv('data/df_final_scoress.csv')
    ideaa=tdf[tdf['ID']==id]
    bi_score=ideaa.iloc[0]['Cost_Score']*10
    roi_score=ideaa.iloc[0]['ROI_Score']*10
    sa_score=ideaa.iloc[0]['SA_Score']*10

    idea = df[df['ID'] == id]
    if not idea.empty:
        comment_str = id_to_comments.get(id, "[]")
        comments = ast.literal_eval(comment_str) if isinstance(comment_str, str) else comment_str

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
            dep_titles=dep_titles,
            bi_score=round(bi_score,2),
            roi_score=round(roi_score,2),
            sa_score=round(sa_score,2)
        )
    else:
        return jsonify({"error": "Idea not found"}), 404
    
@app.route("/cot/<string:id>")
def draw(id):
    buf = cot(id)
    return Response(buf.getvalue(), mimetype='image/jpeg')

@app.route("/powerbi-dashboard")
def powerbi_dashboard():
    return render_template("base.html")