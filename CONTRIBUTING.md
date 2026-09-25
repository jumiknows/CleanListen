# Contributing

CleanListen is a small accessibility and ML project. Prefer focused changes that can be measured.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

On Windows, activate with:

```text
.venv\Scripts\activate
```

## Before a pull request

Run:

```bash
ruff check src tests
pytest -q
```

Good contributions include:

- labelled examples from redistributable public papers
- document IDs for grouped evaluation
- extraction fixes with regression tests
- benchmark improvements
- accessibility feedback from real listening workflows

Do not commit private papers or copyrighted source files unless redistribution is allowed.

When changing the classifier, explain how the change affects both content preservation and noise removal.
