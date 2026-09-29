import requests

from app.config import Config


GROQ_URL = (
    "https://api.groq.com/openai/v1/chat/completions"
)


SYSTEM_PROMPT = """
You are an AI web search assistant.

Answer the user's question using the provided
web search sources.

Rules:

1. Use the sources as your primary evidence.
2. Do not invent information.
3. If the sources are insufficient, say so.
4. Keep the answer clear and useful.
5. Cite sources using [1], [2], [3], etc.
6. Make sure every citation corresponds to the
   correct source.
7. If sources disagree, mention the disagreement.
"""


def generate_answer(query: str, sources: list):

    context_parts = []

    # Keep the total context reasonably small.
    max_total_chars = 30000

    current_chars = 0

    for index, source in enumerate(
        sources,
        start=1
    ):

        # Prefer the normal search result content.
        # It is much smaller than raw webpage HTML/text.
        content = source.get("content", "")

        if not content:
            content = source.get(
                "raw_content",
                ""
            )

        # Limit each individual source.
        content = content[:4000]

        source_text = f"""
SOURCE [{index}]

Title:
{source.get("title", "Untitled")}

URL:
{source.get("url", "")}

Content:
{content}
"""

        # Prevent the complete request from becoming huge.
        if current_chars + len(source_text) > max_total_chars:
            break

        context_parts.append(source_text)
        current_chars += len(source_text)

    context = "\n".join(context_parts)

    user_prompt = f"""
User question:

{query}

Web search sources:

{context}

Using the sources above, answer the user's question.
"""

    payload = {
        "model": Config.LLM_MODEL,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        "temperature": 0.2,
        "max_tokens": 1500
    }

    headers = {
        "Authorization":
            f"Bearer {Config.GROQ_API_KEY}",
        "Content-Type":
            "application/json"
    }

    try:
        response = requests.post(
            GROQ_URL,
            headers=headers,
            json=payload,
            timeout=60
        )

    except requests.RequestException as error:
        raise RuntimeError(
            f"Could not connect to Groq: {error}"
        )

    if response.status_code != 200:

        try:
            error_data = response.json()
        except ValueError:
            error_data = response.text

        raise RuntimeError(
            f"Groq API error "
            f"({response.status_code}): "
            f"{error_data}"
        )

    data = response.json()

    return data["choices"][0]["message"]["content"]