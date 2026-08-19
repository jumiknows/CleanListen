from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from .schema import detect_schema, normalize_label

MODEL_FORMAT_VERSION = 1


@dataclass(frozen=True)
class Prediction:
    text: str
    keep_probability: float
    keep: bool


@dataclass(frozen=True)
class TrainingSummary:
    rows: int
    keep_rows: int
    skip_rows: int
    text_col: str
    label_col: str


def build_pipeline() -> Pipeline:
    """Return the small, interpretable baseline used by the productized CLI."""
    return Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    ngram_range=(1, 2),
                    min_df=1,
                    max_features=30_000,
                    sublinear_tf=True,
                ),
            ),
            (
                "classifier",
                LogisticRegression(
                    max_iter=2_000,
                    class_weight="balanced",
                    random_state=42,
                ),
            ),
        ]
    )


def _payload(model: Pipeline, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "format_version": MODEL_FORMAT_VERSION,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "model": model,
        "metadata": metadata or {},
    }


def save_model(model: Pipeline, model_path: str | Path, metadata: dict[str, Any] | None = None) -> None:
    path = Path(model_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(_payload(model, metadata), path)


def load_model(model_path: str | Path) -> Pipeline:
    """Load current model bundles and older plain-Pipeline artifacts."""
    loaded = joblib.load(model_path)
    if isinstance(loaded, Pipeline):
        return loaded
    if isinstance(loaded, dict) and isinstance(loaded.get("model"), Pipeline):
        return loaded["model"]
    raise ValueError("Unsupported CleanListen model artifact")


def train_csv(
    csv_path: str | Path,
    model_path: str | Path,
    text_col: str | None = None,
    label_col: str | None = None,
) -> TrainingSummary:
    frame = pd.read_csv(csv_path)
    schema = detect_schema(frame, text_col=text_col, label_col=label_col)

    texts = frame[schema.text_col].fillna("").astype(str)
    labels = frame[schema.label_col].map(normalize_label)

    if labels.nunique() < 2:
        raise ValueError("Training data must contain both KEEP and SKIP examples")

    model = build_pipeline()
    model.fit(texts, labels)
    summary = TrainingSummary(
        rows=len(frame),
        keep_rows=int((labels == 1).sum()),
        skip_rows=int((labels == 0).sum()),
        text_col=schema.text_col,
        label_col=schema.label_col,
    )
    save_model(model, model_path, metadata={"training_summary": summary.__dict__})
    return summary


def predict_lines(lines: Sequence[str], model: Pipeline, threshold: float = 0.5) -> list[Prediction]:
    if not 0.0 <= threshold <= 1.0:
        raise ValueError("threshold must be between 0 and 1")
    if not lines:
        return []

    probabilities = model.predict_proba(list(lines))[:, 1]
    return [
        Prediction(text=line, keep_probability=float(score), keep=bool(score >= threshold))
        for line, score in zip(lines, probabilities)
    ]


def keep_lines(lines: Sequence[str], model: Pipeline, threshold: float = 0.5) -> list[str]:
    return [prediction.text for prediction in predict_lines(lines, model, threshold) if prediction.keep]
