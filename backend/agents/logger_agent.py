from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

from backend.config import OPENAI_API_KEY
from backend.tools.file_writer import save_support_log

def create_logger_agent():
    model_client = OpenAIChatCompletionClient(
        model="gpt-5-mini",
        api_key=OPENAI_API_KEY
    )

    logger_agent = AssistantAgent(
        name="logger_agent",
        model_client=model_client,
        tools=[save_support_log],
        reflect_on_tool_use=True,
        system_message="""
            You are a customer support finalizer agent.

            Your job is to receive:
            - the original user query
            - the direct answer from Agent 1
            - the researched answer from Agent 2

            Then prepare a clean final response for the user.

            Rules:
            - Do not search the web.
            - Do not invent new facts.
            - Preserve both answers clearly.
            - Format the final response so it is easy to read.
            """
    )
    return logger_agent