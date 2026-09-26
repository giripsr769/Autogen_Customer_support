import asyncio

from backend.agents.logger_agent import create_logger_agent

async def main():
    agent = create_logger_agent()

    task = """
        User Query:
        My payment was deducted but my order was not confirmed.

        Agent 1 - Direct Answer:
        Please check your order history and payment status. If the order is not visible, contact support with the transaction details.

        Agent 2 - Researched Answer:
        According to the latest support guidance, users should verify payment status and contact support if the transaction succeeded but the order is missing.
    """

    result = await agent.run(task=task)

    print(result.messages[-1].content)

if __name__ == "__main__":
    asyncio.run(main())