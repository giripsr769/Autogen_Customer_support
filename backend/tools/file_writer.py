from datetime import datetime
from pathlib import Path

def save_support_log(
    user_query: str,
    direct_answer: str,
    researched_answer: str
    ) -> str:
    
    log_file = Path("backend/data/support_log.txt")

    log_file.parent.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    content = f"""
        ==================================================
        Timestamp: {timestamp}

        User Query:
        {user_query}

        Agent 1 - Direct Answer:
        {direct_answer}

        Agent 2 - Researched Answer:
        {researched_answer}

        ==================================================

    """

    with open(log_file, "a", encoding="utf-8") as file:
        file.write(content)

    return "Support conversation saved successfully."