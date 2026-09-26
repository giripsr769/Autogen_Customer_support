import asyncio

from backend.agents.support_agent import create_support_agent

async def main():
    agent = create_support_agent()

    result = await agent.run(
        task="My payment was deducted but my order was not confirmed. What should I do?"
    )

    print(result.messages[-1].content)

if __name__ == "__main__":
    asyncio.run(main())