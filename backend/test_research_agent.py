import asyncio

from backend.agents.research_agent import create_research_agent

async def main():
    agent = create_research_agent()

    result = await agent.run(
        task="What is the latest stable Microsoft AutoGen AgentChat documentation?"
    )

    print(result.messages[-1].content)

if __name__ == "__main__":
    asyncio.run(main())