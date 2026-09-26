import requests

from backend.config import SERPER_API_KEY
from duckduckgo_search import DDGS

def search_web(query: str) -> str:
    try:
        url = "https://google.serper.dev/search"

        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        }

        payload = {
            "q": query
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        results = []

        for item in data.get("organic", [])[:5]:
            results.append(
                f"Title: {item.get('title')}\n"
                f"Link: {clean_url(item.get('link'))}\n"
                f"Snippet: {item.get('snippet')}\n"
            )

        if results:
            return "\n".join(results)
        
    except Exception as serper_error:
        print(f"Serper failed: {serper_error}")

    # Fallback to DuckDuckGo
    try:
        results = []

        with DDGS() as ddgs:
            search_results = ddgs.text(
                query,
                max_results=5
            )

            for item in search_results:
                results.append(
                    f"Title: {item.get('title')}\n"
                    f"Link: {clean_url(item.get('href'))}\n"
                    f"Snippet: {item.get('body')}\n"
                )

        if results:
            return "\n".join(results)

    except Exception as duckduckgo_error:
        print(f"DuckDuckGo failed: {duckduckgo_error}")

    return "Web search failed. No search results are available."

def clean_url(url: str) -> str:
    if not url:
        return ""

    return url.replace("https://", "__HTTPS__").replace("http://", "__HTTP__") \
              .replace("//", "/") \
              .replace("__HTTPS__", "https://") \
              .replace("__HTTP__", "http://")