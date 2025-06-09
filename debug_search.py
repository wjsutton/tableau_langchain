import os
from dotenv import load_dotenv

# Import LangSmith tracing (debugging in LangSmith.com)
from langsmith import Client

# Langgraph packages
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from experimental.tools.search_datasource import initialize_datasource_search

from utilities.chat import print_stream
from utilities.prompt import AGENT_SYSTEM_PROMPT

# Load environment
load_dotenv()

# Add LangSmith tracing
langsmith_client = Client()

config = {
    "run_name": "Tableau Langchain Main.py"
}

# # Initialize the Tableau data source tool
# analyze_datasource = initialize_simple_datasource_qa(
#     domain=os.environ['TABLEAU_DOMAIN'],
#     site=os.environ['TABLEAU_SITE'],
#     jwt_client_id=os.environ['TABLEAU_JWT_CLIENT_ID'],
#     jwt_secret_id=os.environ['TABLEAU_JWT_SECRET_ID'],
#     jwt_secret=os.environ['TABLEAU_JWT_SECRET'],
#     tableau_api_version=os.environ['TABLEAU_API_VERSION'],
#     tableau_user=os.environ['TABLEAU_USER'],
#     datasource_luid=os.environ['DATASOURCE_LUID'],
#     # model_provider="openai",
#     tooling_llm_model="gpt-4.1-nano"
# )

# search_datasource = initialize_datasource_search(
#     domain=os.environ['TABLEAU_DOMAIN'],
#     site=os.environ['TABLEAU_SITE'],
#     jwt_client_id=os.environ['TABLEAU_JWT_CLIENT_ID'],
#     jwt_secret_id=os.environ['TABLEAU_JWT_SECRET_ID'],
#     jwt_secret=os.environ['TABLEAU_JWT_SECRET'],
#     tableau_api_version=os.environ['TABLEAU_API_VERSION'],
#     tableau_user=os.environ['TABLEAU_USER'],
#     datasource_luid=os.environ['DATASOURCE_LUID'],
#     # model_provider="openai",
#     tooling_llm_model="gpt-4.1-nano"
# )

from experimental.utilities.auth import jwt_connected_app

print(os.getenv('TABLEAU_DOMAIN'))

auth_token = jwt_connected_app(
                    jwt_client_id=os.getenv('TABLEAU_JWT_CLIENT_ID'),
                    jwt_secret_id=os.getenv('TABLEAU_JWT_SECRET_ID'),
                    jwt_secret=os.getenv('TABLEAU_JWT_SECRET'),
                    tableau_domain=os.getenv('TABLEAU_DOMAIN'),
                    tableau_site=os.getenv('SITE_NAME'),
                    tableau_user=os.getenv('TABLEAU_USER'),
                    tableau_api=os.getenv('TABLEAU_API_VERSION', '3.21'),
                    scopes=["tableau:content:read", "tableau:viz_data_service:read"]
                )

print(auth_token)


search_datasource = initialize_datasource_search()

# Create the agent
llm = ChatOpenAI(model="gpt-4.1", temperature=0)
tools = [search_datasource]

TableauLangChain = create_react_agent(
    model = llm, 
    tools = tools,
    prompt=AGENT_SYSTEM_PROMPT)
    
# # Usage
# your_prompt = 'Find Healthcare datasets'

# # Run the agent
# messages = {"messages": [("user", your_prompt)]}
# print_stream(TableauLangChain.stream(messages, config=config, stream_mode="values"))

