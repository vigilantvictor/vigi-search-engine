import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    LLM_MODEL = os.getenv(
        "LLM_MODEL",
        "openai/gpt-oss-20b"
    )

    MAX_SEARCH_RESULTS = int(
        os.getenv("MAX_SEARCH_RESULTS", "6")
    )

    MAX_SOURCE_LENGTH = int(
        os.getenv("MAX_SOURCE_LENGTH", "12000")
    )

    @classmethod
    def validate(cls):
        missing = []

        if not cls.TAVILY_API_KEY:
            missing.append("TAVILY_API_KEY")

        if not cls.GROQ_API_KEY:
            missing.append("GROQ_API_KEY")

        if missing:
            raise RuntimeError(
                "Missing environment variables: "
                + ", ".join(missing)
            )