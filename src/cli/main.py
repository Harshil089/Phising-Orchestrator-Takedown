# src/cli/main.py
from typing import Optional
import typer
from src.app.config import get_config
from src.discovery.feeds import load_findings_from_csv, write_findings_jsonl

app = typer.Typer(help="Phishing Takedown Orchestrator CLI")

@app.command()
def show_config(config_yaml: Optional[str] = typer.Option(None, help="Path to YAML config")) -> None:
    """Print effective config as JSON."""
    cfg = get_config(config_yaml)
    typer.echo(cfg.to_json())

@app.command()
def discover(
    csv_path: str = typer.Option(..., "--csv", "-c", help="Path to seed CSV"),
    out_path: str = typer.Option("runs/findings.jsonl", "--out", "-o", help="Output JSONL path")
) -> None:
    """Read URLs from CSV, deduplicate, validate, write Findings JSONL."""
    findings = load_findings_from_csv(csv_path)
    typer.echo(f"Loaded {len(findings)} findings.")
    write_findings_jsonl(findings, out_path)
    typer.echo(f"Wrote findings to: {out_path}")

if __name__ == "__main__":
    app()
