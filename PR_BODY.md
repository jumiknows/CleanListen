## Summary

Productizes the original CleanListen notebook into a small, reproducible Python tool without replacing the research prototype.

### What changed

- adds a `src/cleanlisten` package and `cleanlisten` CLI
- adds `train`, `clean`, and `benchmark` workflows
- supports common existing CSV column names automatically
- stores model metadata while remaining compatible with old pipeline artifacts
- adds document-grouped evaluation when document IDs are available
- adds JSON benchmark and cleaning reports
- adds tests, Ruff, and GitHub Actions for Python 3.10 / 3.12
- rewrites the README around the accessibility problem, usage, evidence, and limitations
- adds architecture and benchmarking documentation

### Why

The existing notebook contains promising ML/accessibility work, but the repository is difficult to evaluate as a software project. This keeps the original notebook and data intact while making the core workflow installable, testable, and reproducible.

### Validation

- `pytest -q`
- `ruff check src tests`
- `cleanlisten benchmark examples/sample_labeled_lines.csv`

### Important evidence note

The 91.2% accuracy / 89.7% KEEP F1 / 94.0% specificity numbers remain labeled as **original prototype results**. This PR does not claim they generalize to unseen papers. The next evidence milestone is a document-grouped benchmark across a larger public corpus.
