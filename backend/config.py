import os
from dotenv import load_dotenv


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")


def validate_environment():
    missing_keys = []

    if not OPENAI_API_KEY:
        missing_keys.append("OPENAI_API_KEY")

    if not SERPER_API_KEY:
        missing_keys.append("SERPER_API_KEY")

    if missing_keys:
        raise ValueError(
            f"Missing environment variables: {', '.join(missing_keys)}"
        )

    return True