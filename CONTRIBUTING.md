# Contributing

CleanListen is an accessibility-oriented research prototype becoming a reproducible tool. Small, testable improvements are preferred over large rewrites.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
python -m pip install -e ".[dev]"
pytest -q
ruff check src tests
```

## Good contributions

- more representative labeled lines from public research PDFs
- document identifiers that enable grouped evaluation
- extraction fixes with regression tests
- accessibility feedback from screen-reader or TTS workflows
- benchmark and documentation improvements

## Before opening a pull request

1. Keep private or copyrighted source material out of the repository unless redistribution is allowed.
2. Add or update tests for behavior changes.
3. Run `ruff check src tests` and `pytest -q`.
4. Explain how the change affects content preservation, noise removal, or reproducibility.
