import pandas as pd
import pytest

from cleanlisten.schema import detect_schema, normalize_label


def test_schema_detects_common_aliases():
    frame = pd.DataFrame({"line": ["hello"], "decision": ["KEEP"], "paper_id": ["p1"]})
    schema = detect_schema(frame)
    assert schema.text_col == "line"
    assert schema.label_col == "decision"
    assert schema.group_col == "paper_id"


def test_schema_detects_paper_as_document_group():
    frame = pd.DataFrame({"text": ["hello"], "label": ["KEEP"], "paper": ["p1"]})
    schema = detect_schema(frame)
    assert schema.group_col == "paper"


@pytest.mark.parametrize("value", ["KEEP", "keep", 1, True, "content"])
def test_keep_labels(value):
    assert normalize_label(value) == 1


@pytest.mark.parametrize("value", ["SKIP", "skip", 0, False, "noise"])
def test_skip_labels(value):
    assert normalize_label(value) == 0
