# CleanListen

CleanListen removes layout noise from research PDFs so they are easier to hear through text-to-speech and screen readers.

It does not summarize or rewrite the paper. It decides which extracted lines should be kept.

## What it removes

Typical noise includes:

- page numbers
- publisher headers and footers
- URLs
- repeated conference text
- isolated figure labels
- other layout fragments that interrupt listening

## Quick start

Install the project:

```bash
python -m pip install -e ".[dev]"
```

Train a model:

```bash
cleanlisten train data/labeled_lines.csv \
  --model artifacts/cleanlisten.joblib
```

Clean a PDF:

```bash
cleanlisten clean data/paper1.pdf \
  --model artifacts/cleanlisten.joblib \
  --output outputs/paper1.txt
```

Run the benchmark:

```bash
cleanlisten benchmark data/labeled_lines.csv \
  --json reports/benchmark.json
```

## How it works

The current model is intentionally small:

1. `pdfplumber` extracts text lines from the PDF.
2. TF-IDF converts each line into text features.
3. Logistic regression estimates whether the line should be kept.
4. Lines above the selected threshold are written to the cleaned text file.

The original notebook is kept as the research record. The reusable code lives in `src/cleanlisten`.

## Current data

The checked-in labelled dataset currently contains 631 lines from two papers.

That is enough for a prototype, but not enough to claim broad performance across research PDFs.

The original notebook reported:

| Metric | Prototype result |
| --- | ---: |
| Accuracy | 91.2% |
| KEEP precision | 91.9% |
| KEEP recall | 87.6% |
| KEEP F1 | 89.7% |
| Noise specificity | 94.0% |

These numbers describe the original experiment. They are not a claim about unseen papers.

The next useful evaluation is a document-level benchmark across a much larger public corpus.

## Repository

```text
src/cleanlisten/       package and CLI
tests/                 automated tests
data/                  prototype data
examples/              small schema example
notebook/              original exploration
docs/                  architecture and benchmarking notes
```

## Tests

```bash
ruff check src tests
pytest -q
```

GitHub Actions runs the same checks on Python 3.10 and 3.12.

## Current limits

- Only text-based PDFs are supported.
- OCR is not part of the current pipeline.
- The labelled dataset is small.
- The current evidence is not yet strong enough to claim reliable performance across publishers or disciplines.
- Removing real research content is more harmful than leaving a little noise, so future threshold tuning should favour high KEEP recall.

## Next work

The next milestones are:

1. build a 25+ document public benchmark
2. keep complete papers separate between training and testing
3. record source and redistribution information for benchmark documents
4. tune the decision threshold for high content recall
5. test the listening workflow with real screen-reader and TTS users
6. add a small before and after demo

## Why this project exists

A summary is useful when someone wants a summary.

CleanListen solves a different problem: make the original paper less frustrating to listen to while keeping its methods, results, limitations and argument intact.
