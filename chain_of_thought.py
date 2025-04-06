import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import pandas as pd
import io

def chain_of_thought(idea_id):
    # Read data
    df = pd.read_csv("/Users/hoosiersaikap251/dataviz/docs/df_final_scores.csv")

    # Lookup row
    row = df[df["ID"] == idea_id]
    if row.empty:
        raise ValueError(f"No entry found for ID: {idea_id}")

    # Extract values
    cost_score = row["Cost_Score"].values[0].round(2)
    roi_score = row["ROI_Score"].values[0].round(2)
    sa_score = row["SA_Score"].values[0].round(2)
    upvotes = row["Upvotes"].values[0]
    novelty_score = row["innovation_score"].values[0]

    # Create graph and layout
    G = nx.DiGraph()
    nodes = {
        "Start": "Start Evaluation",
        "Step1": f"The idea has positive\nsentiment with \nUpvotes = {upvotes}\nand Novelty Score = {novelty_score}",
        "Step2": f"Positive Business\nImpact of = {cost_score}",
        "Step3": f"It has an ROI\nIndex of = {roi_score}",
        "Step4": f"It has a Strategic\nAlignment Index = {sa_score}",
        "End": "End: Prioritised Idea"
    }

    for key, label in nodes.items():
        G.add_node(key, label=label)

    edges = [("Start", "Step1"), ("Step1", "Step2"), ("Step2", "Step3"),
             ("Step3", "Step4"), ("Step4", "End")]
    G.add_edges_from(edges)

    pos = {
        "Start": (0, 0),
        "Step1": (4, 0),
        "Step2": (8, 0),
        "Step3": (12, 0),
        "Step4": (16, 0),
        "End":   (20, 0)
    }

    # Create image in memory
    fig, ax = plt.subplots(figsize=(12, 2))
    ax.set_title("Idea Evaluation Flowchart", fontsize=12)

    # Draw boxes
    for node, (x, y) in pos.items():
        label = G.nodes[node]['label']
        width = 3.2
        height = 1.5
        rect = FancyBboxPatch(
            (x - width / 2, y - height / 2),
            width,
            height,
            boxstyle="round,pad=0.02",
            edgecolor='black',
            facecolor='lightblue'
        )
        ax.add_patch(rect)
        ax.text(x, y, label, ha='center', va='center', fontsize=8)

    # Draw arrows
    for src, dst in edges:
        x1, y1 = pos[src]
        x2, y2 = pos[dst]
        arrow = FancyArrowPatch(
            (x1 + 1.6, y1), (x2 - 1.6, y2),
            connectionstyle="arc3,rad=0.0",
            arrowstyle="->",
            mutation_scale=20,
            color='gray',
            linewidth=1.5
        )
        ax.add_patch(arrow)

    ax.set_xlim(-2, 22)
    ax.set_ylim(-2, 2)
    ax.axis('off')

    plt.tight_layout()

    # Save image to in-memory buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='jpg', dpi=300)
    plt.close(fig)
    buf.seek(0)

    return buf