import typer
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from .processor import StructureEngine
from .models import StructuredOutput
import os
import json

app = typer.Typer()
console = Console()

@app.command()
def capture(text: str = typer.Argument(..., help="The raw thought to capture")):
    """
    Capture a raw thought and structure it using the Adaptive AI Second-Brain.
    """
    try:
        # Connect to Docker Qdrant if running, else defaults to localhost
        engine = StructureEngine()
        with console.status("[bold green]Processing and Storing thought..."):
            result = engine.process_thought(text)
        
        # Display results
        rprint("\n[bold blue]Structured Output:[/bold blue]")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Category")
        table.add_column("Title")
        table.add_column("Urgency")
        table.add_column("Importance")
        table.add_column("Context")
        table.add_column("Energy")

        for item in result.items:
            context_str = ", ".join([c.value for c in item.context_tags])
            table.add_row(
                item.category.value,
                item.title,
                item.urgency.value,
                str(item.importance),
                context_str,
                item.energy_level.value
            )
        
        console.print(table)
        rprint("[green]Thought stored in Vector DB.[/green]")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")

@app.command()
def search(query: str = typer.Argument(..., help="Search query for semantic retrieval")):
    """
    Semantically search stored thoughts.
    """
    try:
        engine = StructureEngine()
        with console.status("[bold green]Searching..."):
            results = engine.search_thoughts(query)
        
        rprint(f"\n[bold blue]Search Results for '{query}':[/bold blue]")
        
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Title")
        table.add_column("Description")
        table.add_column("Category")
        
        for res in results:
            table.add_row(
                res.get('title', 'N/A'),
                res.get('description', 'N/A'),
                res.get('category', 'N/A')
            )
        
        console.print(table)

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")

if __name__ == "__main__":
    app()
