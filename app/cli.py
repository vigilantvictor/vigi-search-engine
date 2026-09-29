import webbrowser

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from app.config import Config
from app.database import (
    initialize_database,
    save_search,
    get_history,
    clear_history
)
from app.search import search_web
from app.llm import generate_answer


console = Console()


def show_banner():
    console.print(
        Panel.fit(
            "[bold cyan]VIGI PERSONAL AI SEARCH ENGINE[/bold cyan]\n"
            "[dim]Web Search + AI + Sources[/dim]",
            border_style="cyan"
        )
    )


def show_help():
    console.print("""
[bold cyan]Commands[/bold cyan]

/search <query>     Search the web
/ask <question>     Search + AI answer
/history            Show search history
/clear              Clear search history
/help               Show help
/exit               Exit

You can also type a question directly.
""")


def display_results(results):
    console.print(
        "\n[bold cyan]SEARCH RESULTS[/bold cyan]"
    )

    console.print(
        "[dim]" + "─" * 60 + "[/dim]"
    )

    for index, source in enumerate(
        results,
        start=1
    ):
        console.print(
            f"\n[yellow][{index}][/yellow] "
            f"[bold]{source['title']}[/bold]"
        )

        console.print(
            f"    [blue]{source['url']}[/blue]"
        )

    console.print(
        "\n[dim]" + "─" * 60 + "[/dim]"
    )


def show_result_menu():
    console.print("""
[bold]What would you like to do?[/bold]

[a]  AI Answer
[1-6] Select a source
[n]  New search
[h]  History
[q]  Quit
""")


def open_source(source):
    console.print(
        f"\n[cyan]Opening:[/cyan] "
        f"{source['title']}"
    )

    console.print(
        f"[blue]{source['url']}[/blue]\n"
    )

    webbrowser.open(source["url"])


def show_source(source, index):

    console.print()

    console.print(
        Panel(
            f"[bold]{source['title']}[/bold]\n\n"
            f"[blue]{source['url']}[/blue]\n\n"
            f"{source.get('content', 'No preview available.')}",
            title=f"Source [{index}]",
            border_style="yellow"
        )
    )


def source_menu(source, index):

    while True:

        console.print("""
[bold]Source options[/bold]

[a]  Ask AI about this source
[o]  Open in browser
[b]  Back to results
[q]  Quit
""")

        choice = console.input(
            "[bold cyan]Source > [/bold cyan]"
        ).strip().lower()

        # Ask AI
        if choice in (
            "a",
            "ask",
            "ask ai",
            "ask ai about this source"
        ):

            question = console.input(
                "\n[bold cyan]Question > [/bold cyan]"
            ).strip()

            if not question:
                console.print(
                    "[yellow]Please enter a question.[/yellow]"
                )
                continue

            console.print(
                "\n[cyan]🤖 Analyzing source...[/cyan]"
            )

            try:

                answer = generate_answer(
                    question,
                    [source]
                )

                console.print(
                    Panel(
                        answer,
                        title="🤖 AI Answer",
                        border_style="green"
                    )
                )

            except Exception as error:

                console.print(
                    f"[red]LLM request failed:[/red] "
                    f"{error}"
                )

        # Open source
        elif choice in (
            "o",
            "open",
            "open in browser"
        ):

            open_source(source)

        # Back
        elif choice in (
            "b",
            "back",
            "back to results"
        ):

            return "back"

        # Quit
        elif choice in (
            "q",
            "quit",
            "exit"
        ):

            return "quit"

        else:

            console.print(
                "[yellow]Invalid option. "
                "Use a, o, b, or q.[/yellow]"
            )


def ai_answer(query, results):

    console.print(
        "\n[cyan]🤖 Analyzing sources...[/cyan]"
    )

    try:

        answer = generate_answer(
            query,
            results
        )

    except Exception as error:

        console.print(
            f"[red]LLM request failed:[/red] "
            f"{error}"
        )

        return None

    console.print()

    console.print(
        Panel(
            answer,
            title="🤖 AI Answer",
            border_style="green"
        )
    )

    return answer

def perform_search(query):

    console.print(
        "\n[cyan]🔎 Searching the web...[/cyan]"
    )

    try:

        results = search_web(query)

    except Exception as error:

        console.print(
            f"[red]Search failed:[/red] {error}"
        )

        return

    if not results:

        console.print(
            "[yellow]No results found.[/yellow]"
        )

        return

    console.print(
        f"[green]✓ Found {len(results)} sources[/green]"
    )

    display_results(results)

    while True:

        show_result_menu()

        choice = console.input(
            "[bold cyan]> [/bold cyan]"
        ).strip().lower()

        # --------------------------------
        # AI ANSWER
        # --------------------------------

        if choice in (
            "a",
            "ai",
            "ai answer"
        ):

            answer = ai_answer(
                query,
                results
            )

            if answer:

                save_search(
                    query,
                    answer
                )

        # --------------------------------
        # QUIT
        # --------------------------------

        elif choice in (
            "q",
            "quit",
            "exit"
        ):

            return "quit"

        # --------------------------------
        # NEW SEARCH
        # --------------------------------

        elif choice in (
            "n",
            "new",
            "new search"
        ):

            return "new"

        # --------------------------------
        # HISTORY
        # --------------------------------

        elif choice in (
            "h",
            "history"
        ):

            show_history()

        # --------------------------------
        # SOURCE SELECTION
        # --------------------------------

        elif choice.isdigit():

            source_number = int(choice)

            if (
                1 <= source_number
                <= len(results)
            ):

                source = results[
                    source_number - 1
                ]

                show_source(
                    source,
                    source_number
                )

                result = source_menu(
                    source,
                    source_number
                )

                if result == "quit":

                    return "quit"

            else:

                console.print(
                    "[yellow]"
                    "Invalid source number."
                    "[/yellow]"
                )

        # --------------------------------
        # UNKNOWN COMMAND
        # --------------------------------

        else:

            console.print(
                "[yellow]"
                "Invalid option. "
                "Use a, 1-6, n, h, or q."
                "[/yellow]"
            )


def show_history():

    history = get_history()

    if not history:

        console.print(
            "[yellow]No search history.[/yellow]"
        )

        return

    table = Table(
        title="Search History"
    )

    table.add_column(
        "ID",
        style="cyan"
    )

    table.add_column(
        "Query",
        style="white"
    )

    table.add_column(
        "Date",
        style="dim"
    )

    for row in history:

        table.add_row(
            str(row[0]),
            row[1],
            row[2]
        )

    console.print(table)


def run():

    Config.validate()

    initialize_database()

    show_banner()

    show_help()

    while True:

        try:

            user_input = console.input(
                "\n[bold cyan]Search > [/bold cyan]"
            ).strip()

        except KeyboardInterrupt:

            console.print(
                "\n[yellow]Goodbye! 👋[/yellow]"
            )

            break

        if not user_input:
            continue

        if user_input == "/exit":

            console.print(
                "[yellow]Goodbye! 👋[/yellow]"
            )

            break

        if user_input == "/help":

            show_help()
            continue

        if user_input == "/history":

            show_history()
            continue

        if user_input == "/clear":

            clear_history()

            console.print(
                "[green]History cleared.[/green]"
            )

            continue

        if user_input.startswith("/search "):

            query = user_input[
                len("/search "):
            ].strip()

            if query:
                result = perform_search(
                    query
                )

                if result == "quit":
                    break

            continue

        if user_input.startswith("/ask "):

            query = user_input[
                len("/ask "):
            ].strip()

            if query:
                result = perform_search(
                    query
                )

                if result == "quit":
                    break

            continue

        # Normal input
        result = perform_search(
            user_input
        )

        if result == "quit":
            break