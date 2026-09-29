from app.database import (
    initialize_database,
    save_search,
    get_history
)


def test_database():
    initialize_database()

    save_search(
        "test query",
        "test answer"
    )

    history = get_history()

    assert len(history) > 0