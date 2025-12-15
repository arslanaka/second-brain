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
        engine = StructureEngine()
        with console.status("[bold green]Processing thought..."):
            result = engine.process_thought(text)
        
        # Display results
        rprint("\n[bold blue]Structured Output:[/bold blue]")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Category")
        table.add_column("Title")
        table.add_column("Urgency")
        table.add_column("Next Step")
        table.add_column("Clarity")

        for item in result.items:
            table.add_row(
                item.category.value,
                item.title,
                item.urgency.value,
                item.next_step,
                str(item.clarity_score)
            )
        
        console.print(table)

        # Print detailed JSON
        rprint("\n[bold dim]Raw JSON:[/bold dim]")
        print(result.model_dump_json(indent=2))

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")

if __name__ == "__main__":
    app()
