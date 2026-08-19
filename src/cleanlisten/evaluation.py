from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support
from sklearn.model_selection import GroupShuffleSplit, train_test_split

from .model import build_pipeline
from .schema import detect_schema, normalize_label


@dataclass(frozen=True)
class BenchmarkResult:
    split: str
    train_rows: int
    test_rows: int
    accuracy: float
    precision_keep: float
    recall_keep: float
    f1_keep: float
    specificity_skip: float
    true_skip: int
    false_keep: int
    false_skip: int
    true_keep: int
    text_col: str
    label_col: str
    group_col: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _metrics(
    y_true: list[int],
    y_pred: list[int],
) -> tuple[float, float, float, float, float, int, int, int, int]:
    accuracy = float(accuracy_score(y_true, y_pred))
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true,
        y_pred,
        labels=[1],
        average=None,
        zero_division=0,
    )
    matrix = confusion_matrix(y_true, y_pred, labels=[0, 1])
    true_skip, false_keep, false_skip, true_keep = (int(value) for value in matrix.ravel())
    denom = true_skip + false_keep
    specificity = true_skip / denom if denom else 0.0
    return (
        accuracy,
        float(precision[0]),
        float(recall[0]),
        float(f1[0]),
        float(specificity),
        true_skip,
        false_keep,
        false_skip,
        true_keep,
    )


def benchmark_csv(
    csv_path: str | Path,
    *,
    text_col: str | None = None,
    label_col: str | None = None,
    group_col: str | None = None,
    test_size: float = 0.25,
    random_state: int = 42,
) -> BenchmarkResult:
    if not 0.05 <= test_size <= 0.5:
        raise ValueError("test_size must be between 0.05 and 0.5")

    frame = pd.read_csv(csv_path)
    schema = detect_schema(frame, text_col=text_col, label_col=label_col, group_col=group_col)
    frame = frame.copy()
    frame["__text"] = frame[schema.text_col].fillna("").astype(str)
    frame["__label"] = frame[schema.label_col].map(normalize_label)

    if frame["__label"].nunique() < 2:
        raise ValueError("Benchmark data must contain both KEEP and SKIP examples")

    indices = frame.index.to_numpy()
    split_name: str

    if schema.group_col:
        groups = frame[schema.group_col].fillna("__missing_group__").astype(str)
        if groups.nunique() < 2:
            raise ValueError("Grouped benchmarking requires at least two distinct documents/groups")
        splitter = GroupShuffleSplit(n_splits=1, test_size=test_size, random_state=random_state)
        train_positions, test_positions = next(splitter.split(indices, frame["__label"], groups))
        train_idx, test_idx = indices[train_positions], indices[test_positions]
        split_name = "document-grouped"
    else:
        train_idx, test_idx = train_test_split(
            indices,
            test_size=test_size,
            random_state=random_state,
            stratify=frame["__label"],
        )
        split_name = "line-stratified"

    train = frame.loc[train_idx]
    test = frame.loc[test_idx]

    model = build_pipeline()
    model.fit(train["__text"], train["__label"])
    predictions = model.predict(test["__text"])
    values = _metrics(test["__label"].tolist(), predictions.tolist())

    return BenchmarkResult(
        split=split_name,
        train_rows=len(train),
        test_rows=len(test),
        accuracy=values[0],
        precision_keep=values[1],
        recall_keep=values[2],
        f1_keep=values[3],
        specificity_skip=values[4],
        true_skip=values[5],
        false_keep=values[6],
        false_skip=values[7],
        true_keep=values[8],
        text_col=schema.text_col,
        label_col=schema.label_col,
        group_col=schema.group_col,
    )
