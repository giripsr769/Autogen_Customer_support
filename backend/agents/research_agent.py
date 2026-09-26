from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

from backend.config import OPENAI_API_KEY
from backend.tools.web_search import search_web

def create_research_agent():
    model_client = OpenAIChatCompletionClient(
        model="gpt-5-mini",
        api_key=OPENAI_API_KEY
    )

    research_agent = AssistantAgent(
        name="research_agent",
        model_client=model_client,
        tools=[search_web],
        reflect_on_tool_use=True,
        system_message="""
            You are a customer support research agent.

            Your job is to answer the user's query using web search.

            Rules:
            - Use the search_web tool before answering.
            - Base your answer on the search results.
            - Give a clear and concise response.
            - Include useful source links when relevant.
            - Do not make up information that is not supported by the search results.
            """             
    )

    return research_agent