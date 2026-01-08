from __future__ import annotations

import json
import os
from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console
from rich.table import Table

from .config import load_config
from .engine import AuditEngine
from .formatters.human import HumanFormatter
from .formatters.json import JsonFormatter
from .models import Severity

app = typer.Typer(add_completion=False, help="Rule-based, explainable README auditor.")


def _collect_targets(path: Path) -> List[Path]:
    if path.is_file():
        return [path]
    # directory: audit README files (common convention) and any *.md at root
    candidates: List[Path] = []
    for name in ("README.md", "readme.md", "README.MD", "Readme.md"):
        p = path / name
        if p.exists() and p.is_file():
            candidates.append(p)
    if candidates:
        return candidates
    # fallback: top-level markdown files
    for p in sorted(path.glob("*.md")):
        if p.is_file():
            candidates.append(p)
    return candidates


def _severity(value: str) -> Severity:
    v = value.strip().lower()
    if v not in ("info", "warning", "error"):
        raise typer.BadParameter("Severity must be one of: info, warning, error")
    return v  # type: ignore[return-value]


@app.command()
def main(
    target: Path = typer.Argument(..., help="Path to README.md or a directory"),
    format: str = typer.Option("human", "--format", help="human or json"),
    config: Optional[Path] = typer.Option(None, "--config", help="Path to auditor TOML config"),
    fail_on: str = typer.Option("error", "--fail-on", callback=lambda v: _severity(v), help="info, warning, or error"),
    output: Optional[Path] = typer.Option(None, "--output", help="Write report to file"),
    list_rules: bool = typer.Option(False, "--list-rules", help="List all available rules and exit"),
) -> None:
    cfg = load_config(str(config) if config else None)
    cfg.output_format = format.strip().lower()  # type: ignore[assignment]
    cfg.fail_on = _severity(fail_on)

    engine = AuditEngine(cfg)

    if list_rules:
        con = Console()
        table = Table(title="Available Rules")
        table.add_column("rule_id", style="bold")
        table.add_column("name")
        table.add_column("default severity")
        for rid, name, sev in engine.available_rules():
            table.add_row(rid, name, sev)
        con.print(table)
        raise typer.Exit(code=0)

    if not target.exists():
        raise typer.BadParameter(f"Target does not exist: {target}")

    targets = _collect_targets(target)
    if not targets:
        raise typer.BadParameter(f"No README or markdown files found in: {target}")

    formatter = HumanFormatter(color=cfg.color, show_suggestions=cfg.show_suggestions) if cfg.output_format == "human" else JsonFormatter()

    overall_pass = True
    rendered_outputs: List[str] = []
    for f in targets:
        content = f.read_text(encoding="utf-8")
        report = engine.audit_content(filename=str(f), content=content)
        overall_pass = overall_pass and report.passed
        rendered = formatter.render(report)
        rendered_outputs.append(rendered)
        if output is None:
            formatter.print(report)

    if output is not None:
        joined = "\n\n".join(rendered_outputs)
        output.write_text(joined, encoding="utf-8")

    raise typer.Exit(code=0 if overall_pass else 1)
