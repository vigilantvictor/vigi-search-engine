from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.search import search_web
from app.llm import generate_answer
from app.database import (
    save_search,
    get_history,
    clear_history
)


router = APIRouter(
    prefix="/api"
)


class SearchRequest(BaseModel):
    query: str


class SourceQuestion(BaseModel):
    question: str
    source: dict


@router.post("/search")
def search(request: SearchRequest):

    query = request.query.strip()

    if not query:
        raise HTTPException(
            status_code=400,
            detail="Search query cannot be empty."
        )

    try:

        results = search_web(query)

        if not results:
            return {
                "query": query,
                "answer": "",
                "sources": []
            }

        answer = generate_answer(
            query,
            results
        )

        save_search(
            query,
            answer
        )

        return {
            "query": query,
            "answer": answer,
            "sources": results
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@router.post("/source/ask")
def ask_about_source(
    request: SourceQuestion
):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:

        answer = generate_answer(
            question,
            [request.source]
        )

        return {
            "answer": answer
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@router.get("/history")
def history():

    try:

        results = get_history()

        return {
            "history": [
                {
                    "id": row[0],
                    "query": row[1],
                    "date": row[2]
                }
                for row in results
            ]
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@router.delete("/history")
def delete_history():

    try:

        clear_history()

        return {
            "message": "Search history cleared."
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )