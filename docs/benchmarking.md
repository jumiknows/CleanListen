# Benchmarking

CleanListen should be judged on papers it did not train on.

## Run the current benchmark

```bash
cleanlisten benchmark data/labeled_lines.csv \
  --json reports/benchmark.json
```

The current dataset uses `paper` as its document column, so the CLI treats complete papers as groups.

You can also specify columns directly:

```bash
cleanlisten benchmark data/labeled_lines.csv \
  --text-col text \
  --label-col label \
  --group-col paper \
  --json reports/benchmark.json
```

## Split types

### Document grouped

Use this whenever document IDs are available.

A paper appears in either training or testing, not both.

This is closer to the real task because CleanListen will usually receive a completely new paper.

### Line stratified

This is the fallback when no document column exists.

It is useful during early experiments, but it can make results look better than they are because similar lines from one paper can appear in both sets.

## Metrics

| Metric | What it tells us |
| --- | --- |
| Accuracy | Overall fraction of correct decisions |
| KEEP precision | How often kept lines are real content |
| KEEP recall | How much real content survives cleaning |
| KEEP F1 | Balance of KEEP precision and recall |
| SKIP specificity | How often noise is removed |

For this project, KEEP recall matters most. Removing a real method, result or limitation is usually worse than leaving one extra header in the listening text.

## Stronger evidence

The next benchmark should use at least 25 public papers from different layouts and publishers.

For each paper, record:

- document ID
- public source
- redistribution status
- layout type
- discipline or venue
- labelled line count

The final report should show both aggregate metrics and per-document results.
