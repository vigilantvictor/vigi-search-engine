import requests

from app.config import Config


TAVILY_URL = "https://api.tavily.com/search"


def search_web(query: str):

    query = query.strip()

    if not query:
        return []

    if not Config.TAVILY_API_KEY:
        raise RuntimeError(
            "TAVILY_API_KEY is missing. "
            "Check your .env file."
        )

    payload = {
        "api_key": Config.TAVILY_API_KEY,
        "query": query,
        "search_depth": "basic",
        "max_results": Config.MAX_SEARCH_RESULTS,
        "include_answer": False
    }

    try:
        response = requests.post(
            TAVILY_URL,
            json=payload,
            timeout=30
        )

    except requests.RequestException as error:
        raise RuntimeError(
            f"Could not connect to Tavily: {error}"
        )

    if response.status_code != 200:

        try:
            error_data = response.json()
        except ValueError:
            error_data = response.text

        raise RuntimeError(
            f"Tavily API error "
            f"({response.status_code}): "
            f"{error_data}"
        )

    data = response.json()

    results = []

    for item in data.get("results", []):

        results.append({
            "title": item.get(
                "title",
                "Untitled"
            ),
            "url": item.get(
                "url",
                ""
            ),
            "content": item.get(
                "content",
                ""
            )
        })

    return results