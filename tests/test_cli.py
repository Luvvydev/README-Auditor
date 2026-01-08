from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from readme_auditor.cli import app

runner = CliRunner()


def test_cli_lists_rules():
    result = runner.invoke(app, ["--list-rules", "."])
    assert result.exit_code == 0
    assert "vague_claims" in result.stdout


def test_cli_audits_fixture_good(fixtures_dir: Path):
    good = fixtures_dir / "good_readme.md"
    result = runner.invoke(app, [str(good), "--fail-on", "error"])
    assert result.exit_code == 0


def test_cli_json_output(fixtures_dir: Path):
    vague = fixtures_dir / "vague_readme.md"
    result = runner.invoke(app, [str(vague), "--format", "json", "--fail-on", "warning"])
    assert result.exit_code == 1
    assert '"issues":' in result.stdout


def test_cli_output_file(fixtures_dir: Path, tmp_path: Path):
    good = fixtures_dir / "good_readme.md"
    out = tmp_path / "report.txt"
    result = runner.invoke(app, [str(good), "--output", str(out)])
    assert result.exit_code == 0
    assert out.exists()
    assert "Found" in out.read_text(encoding="utf-8")


def test_cli_directory_scans_readme(tmp_path: Path):
    d = tmp_path / "proj"
    d.mkdir()
    (d / "README.md").write_text(
        "# X\n\n## Installation\n\n```bash\npip install x\n```\n\n## Usage\n\n```bash\nx --help\n```\n\n## Troubleshooting\n\nText\n\n## Limitations\n\nText\n\n## Contributing\n\nText\n\n## License\n\nMIT\n",
        encoding="utf-8",
    )
    result = runner.invoke(app, [str(d)])
    assert result.exit_code == 0


def test_cli_directory_fallback_md(tmp_path: Path):
    d = tmp_path / "proj2"
    d.mkdir()
    (d / "doc.md").write_text(
        "# T\n\n## Installation\n\n```bash\npip install x\n```\n\n## Usage\n\n```bash\nx --help\n```\n\n## Troubleshooting\n\nText\n\n## Limitations\n\nText\n\n## Contributing\n\nText\n\n## License\n\nMIT\n",
        encoding="utf-8",
    )
    result = runner.invoke(app, [str(d)])
    assert result.exit_code == 0


def test_cli_rejects_bad_severity(fixtures_dir: Path):
    good = fixtures_dir / "good_readme.md"
    result = runner.invoke(app, [str(good), "--fail-on", "fatal"])
    assert result.exit_code != 0
