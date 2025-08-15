# src/cli/main.py
from typing import Optional
import typer
from src.app.config import get_config

app = typer.Typer(help="Phishing Takedown Orchestrator CLI")

def _version_callback(value: bool) -> None:
    if value:
        typer.echo("phish-takedown-orchestrator v0.2.0")
        raise typer.Exit()

@app.command(name="show-config")
def show_config(config_yaml: Optional[str] = typer.Option(None, help="Path to YAML config")) -> None:
    """Print effective config as JSON."""
    cfg = get_config(config_yaml)
    typer.echo(cfg.to_json())

@app.command()
def discover() -> None:
    """Discovery step placeholder."""
    typer.echo("Discovery step placeholder")

if __name__ == "__main__":
    app()
