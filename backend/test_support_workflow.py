import asyncio

from backend.services.support_service import run_support_workflow

async def main():
    result = await run_support_workflow(
        "My payment was deducted but my order was not confirmed. What should I do?"
    )

    print(result)

if __name__ == "__main__":
    asyncio.run(main())