# src/cli/main.py
from typing import Optional
import typer

app = typer.Typer(help="Phishing Takedown Orchestrator CLI (Week 1 skeleton)")

def _version_callback(value: bool) -> None:
    if value:
        typer.echo("phish-takedown-orchestrator v0.1.0")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    """Global options for the CLI."""
    return

@app.command()
def discover() -> None:
    """Discovery step placeholder."""
    typer.echo("Discovery step placeholder")

if __name__ == "__main__":
    app()
