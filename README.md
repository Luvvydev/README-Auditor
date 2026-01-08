# README-Auditor

README-Auditor is a Python CLI tool that audits GitHub README files using explicit, rule based checks.
It reports specific findings with the rule id, the reason, and an actionable suggestion.

## Why This Project Exists

Over time I noticed a pattern: genuinely useful projects were being ignored, misunderstood, or misused not because the code was bad, but because the README failed the reader. Missing context. Overconfident claims. Setup steps that assumed prior knowledge. No examples. No limits stated.  

README-Auditor exists to act as a second pair of eyes.

It does not try to write your README for you.  
It does not enforce style, tone, or marketing language.  
It asks questions on behalf of your future users:

- Who is this actually for?
- What assumptions are you making?
- What can this *not* do?
- Are your claims falsifiable?
- Could someone succeed here without already knowing the system?

The goal is respect: respect for the reader’s time, intelligence, and expectations.

If this tool helps even one project avoid confusion, then it has done its job.


## Installation

```bash
python -m pip install readme-auditor
```

For development:

```bash
git clone https://github.com/example/readme-auditor.git
cd README-Auditor
pip install -e ".[dev]"
```

## Usage

Audit a single README:

```bash
readme-auditor README.md
```

Audit a directory (the tool will look for README.md at the root):

```bash
readme-auditor .
```

JSON output for CI:

```bash
readme-auditor README.md --format json --fail-on error
```

List rules:

```bash
readme-auditor . --list-rules
```

## Configuration

Create a TOML file and pass it with `--config`.

```toml
[general]
severity_threshold = "warning"
max_issues = 50
fail_on = "error"

[rules.vague_claims]
enabled = true
custom_adjectives = ["blazing", "next-gen"]

[output]
format = "human"
color = true
show_suggestions = true
```

## Rule Set

The default rule set focuses on clarity, credibility, and completeness.

- vague_claims
- missing_sections
- unfalsifiable
- link_only_setup
- assumed_knowledge
- no_examples
- overpromising
- unclear_audience
- no_troubleshooting
- missing_limitations

## Troubleshooting

- If `readme-auditor` is not found, confirm your virtual environment is active and reinstall with `pip install -e .`.
- If Markdown parsing fails on a file, reduce the file to a minimal reproducer and open an issue with the content.

## Limitations

- The tool only analyzes Markdown files and does not execute code blocks.
- The heuristics are conservative and may produce false positives on marketing style READMEs.
- API reference detection is heuristic and may not apply to all projects.

## Contributing

- Run `pip install -e ".[dev]"`.
- Run `pytest` before opening a pull request.
- Keep rules explainable and add fixture based tests for new heuristics.

## License

MIT
