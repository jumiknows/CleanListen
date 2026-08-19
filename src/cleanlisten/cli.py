from __future__ import annotations

import argparse
import json
from pathlib import Path

from .evaluation import benchmark_csv
from .model import load_model, predict_lines, train_csv
from .pdf import extract_lines


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cleanlisten",
        description=(
            "Clean research PDFs for screen readers and text-to-speech "
            "without summarizing the paper."
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)

    train = sub.add_parser("train", help="Train a line classifier from a labeled CSV")
    train.add_argument("csv", type=Path)
    train.add_argument("--model", type=Path, default=Path("artifacts/cleanlisten.joblib"))
    train.add_argument("--text-col")
    train.add_argument("--label-col")

    clean = sub.add_parser("clean", help="Clean a text-based PDF using a trained model")
    clean.add_argument("pdf", type=Path)
    clean.add_argument("--model", type=Path, default=Path("artifacts/cleanlisten.joblib"))
    clean.add_argument("--output", "-o", type=Path, required=True)
    clean.add_argument("--threshold", type=float, default=0.5)
    clean.add_argument("--stats-json", type=Path)

    benchmark = sub.add_parser("benchmark", help="Run a reproducible held-out benchmark")
    benchmark.add_argument("csv", type=Path)
    benchmark.add_argument("--text-col")
    benchmark.add_argument("--label-col")
    benchmark.add_argument("--group-col")
    benchmark.add_argument("--test-size", type=float, default=0.25)
    benchmark.add_argument("--seed", type=int, default=42)
    benchmark.add_argument("--json", dest="json_path", type=Path)

    return parser


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _run_train(args: argparse.Namespace) -> None:
    summary = train_csv(args.csv, args.model, args.text_col, args.label_col)
    print(
        f"trained on {summary.rows} rows "
        f"({summary.keep_rows} KEEP / {summary.skip_rows} SKIP); saved {args.model}"
    )


def _run_clean(args: argparse.Namespace) -> None:
    model = load_model(args.model)
    lines = extract_lines(args.pdf)
    predictions = predict_lines(lines, model, args.threshold)
    kept = [item.text for item in predictions if item.keep]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(kept) + ("\n" if kept else ""), encoding="utf-8")

    stats = {
        "input_pdf": str(args.pdf),
        "output_text": str(args.output),
        "threshold": args.threshold,
        "input_lines": len(lines),
        "kept_lines": len(kept),
        "removed_lines": len(lines) - len(kept),
        "reduction_fraction": round((len(lines) - len(kept)) / len(lines), 4) if lines else 0.0,
    }
    if args.stats_json:
        _write_json(args.stats_json, stats)
    print(
        f"kept {stats['kept_lines']}/{stats['input_lines']} lines; "
        f"removed {stats['removed_lines']}; wrote {args.output}"
    )


def _run_benchmark(args: argparse.Namespace) -> None:
    result = benchmark_csv(
        args.csv,
        text_col=args.text_col,
        label_col=args.label_col,
        group_col=args.group_col,
        test_size=args.test_size,
        random_state=args.seed,
    )
    payload = result.to_dict()
    print(f"split: {result.split}")
    print(f"accuracy: {result.accuracy:.3f}")
    print(f"KEEP precision: {result.precision_keep:.3f}")
    print(f"KEEP recall: {result.recall_keep:.3f}")
    print(f"KEEP F1: {result.f1_keep:.3f}")
    print(f"SKIP specificity: {result.specificity_skip:.3f}")
    if result.split == "line-stratified":
        print("note: add a document/group column for the stronger document-grouped benchmark")
    if args.json_path:
        _write_json(args.json_path, payload)
        print(f"wrote {args.json_path}")


def main() -> None:
    args = _parser().parse_args()
    if args.command == "train":
        _run_train(args)
    elif args.command == "clean":
        _run_clean(args)
    elif args.command == "benchmark":
        _run_benchmark(args)


if __name__ == "__main__":
    main()
