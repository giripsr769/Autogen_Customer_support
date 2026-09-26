from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

from backend.config import OPENAI_API_KEY

def create_support_agent():
    model_client = OpenAIChatCompletionClient(
        model="gpt-5-mini",
        api_key=OPENAI_API_KEY
    )

    support_agent = AssistantAgent(
        name="support_agent",
        model_client=model_client,
        system_message="""
            You are a helpful customer support agent.

            Your job is to answer the user's query directly using your existing knowledge.

            Rules:
            - Give a clear and concise response.
            - Do not search the web.
            - Do not invent information if you are unsure.
            - Focus only on answering the user's question.
            """
    )

    return support_agent