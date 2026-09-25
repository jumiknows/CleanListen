from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

import pandas as pd

TEXT_ALIASES = ("text", "line", "content", "sentence", "raw_text")
LABEL_ALIASES = ("label", "decision", "class", "target", "keep")
GROUP_ALIASES = ("document_id", "doc_id", "document", "paper_id", "paper", "source")


@dataclass(frozen=True)
class DatasetSchema:
    text_col: str
    label_col: str
    group_col: str | None = None


def _find_column(
    columns: Iterable[str],
    preferred: str | None,
    aliases: tuple[str, ...],
    kind: str,
) -> str:
    available = list(columns)
    if preferred:
        if preferred not in available:
            raise ValueError(f"{kind} column {preferred!r} not found. Available: {available}")
        return preferred

    lower_to_original = {name.lower(): name for name in available}
    for alias in aliases:
        if alias in lower_to_original:
            return lower_to_original[alias]

    raise ValueError(
        f"Could not detect the {kind} column. Pass --{kind}-col explicitly. "
        f"Available columns: {available}"
    )


def detect_schema(
    frame: pd.DataFrame,
    text_col: str | None = None,
    label_col: str | None = None,
    group_col: str | None = None,
) -> DatasetSchema:
    text = _find_column(frame.columns, text_col, TEXT_ALIASES, "text")
    label = _find_column(frame.columns, label_col, LABEL_ALIASES, "label")

    group: str | None = None
    if group_col:
        if group_col not in frame.columns:
            available = list(frame.columns)
            raise ValueError(
                f"group column {group_col!r} not found. Available: {available}"
            )
        group = group_col
    else:
        lower_to_original = {name.lower(): name for name in frame.columns}
        for alias in GROUP_ALIASES:
            if alias in lower_to_original:
                group = lower_to_original[alias]
                break

    return DatasetSchema(text, label, group)


def normalize_label(value: object) -> int:
    if pd.isna(value):
        raise ValueError("Label cannot be empty")

    text = str(value).strip().upper()
    if text in {"KEEP", "1", "TRUE", "YES", "CONTENT", "READ"}:
        return 1
    if text in {"SKIP", "0", "FALSE", "NO", "NOISE", "DROP", "REMOVE"}:
        return 0
    raise ValueError(f"Unsupported label: {value!r}. Expected KEEP/SKIP or 1/0.")
