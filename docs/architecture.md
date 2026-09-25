# Architecture

CleanListen keeps extraction, classification and evaluation separate so each part can be measured.

## Cleaning a paper

1. `pdf.py` extracts non-empty lines from a text-based PDF.
2. `model.py` loads the trained TF-IDF and logistic regression pipeline.
3. Each line receives a KEEP probability.
4. Lines above the selected threshold are written to the output file.
5. Optional JSON stats record how much text was kept and removed.

## Training

`schema.py` finds the text, label and optional document columns in a labelled CSV.

`model.py` trains the classifier and stores the model with basic training metadata.

## Benchmarking

`evaluation.py` supports two split types.

`document-grouped`
Keeps complete documents on one side of the train and test boundary. This is the preferred evaluation.

`line-stratified`
Randomly splits individual lines. This is useful for the early prototype, but it is weaker evidence because lines from the same paper can appear in both sets.

## Why the model is simple

The current dataset is small. TF-IDF with logistic regression is fast, easy to inspect and easy to reproduce.

A larger model is only useful if it improves results on unseen documents.

## OCR

OCR is intentionally separate from the current package. Scanned PDFs introduce an extraction problem that should not be mixed into classifier quality without measuring it separately.
