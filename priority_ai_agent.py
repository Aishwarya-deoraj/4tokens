import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType, Tool
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Load DataFrame only once, avoid loading it repeatedly on imports
df = pd.read_csv('data/df_final_scoress.csv')
df.reset_index(drop=True, inplace=True)

api_key = os.getenv("OPENAI_API_KEY")


pandasai_llm = OpenAI(api_token=api_key)
sdf = SmartDataframe(df, config={"llm": pandasai_llm})

def initialize_langchain():

    langchain_llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0,
        openai_api_key=api_key
    )

    def chat_with_dataframe(query: str) -> str:
        try:
            return str(sdf.chat(query))
        except Exception as e:
            return f"Error: {e}"

    pandasai_tool = Tool(
        name="PandasAI Data Chat",
        func=chat_with_dataframe,
        description="Use this tool to ask questions about the dataset like 'Top 3 rows by ROI', 'Average impact score', etc."
    )


    agent = initialize_agent(
        tools=[pandasai_tool],
        llm=langchain_llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        max_iterations=3
    )

    return agent

agent = None

def get_agent():
    global agent
    if agent is None:
        agent = initialize_langchain()
    return agent

def top3_ideas(roi_score, sa_score, bi_score):
    agent = get_agent()
    qs = f"""
    Given the weights:
    ROI - {roi_score}% ;
    Strategic Alignment - {sa_score}% ;
    Business Impact - {bi_score}% ,
    choose the top 3 ideas to be implemented based on these criteria.
    Return a list of dictionaries where each dictionary contains 'id' and 'title' as keys. 
    The result should be in the following format: 
    [
        {{ "id": "<id1>", "title": "<title1>" }},
        {{ "id": "<id2>", "title": "<title2>" }},
        {{ "id": "<id3>", "title": "<title3>" }}
    ]
    """
    response = agent.run(qs)
    return response
