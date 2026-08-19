from pathlib import Path

import pandas as pd

from cleanlisten.evaluation import benchmark_csv


def test_benchmark_uses_document_groups_when_available(tmp_path: Path):
    rows = []
    for paper in range(8):
        rows.extend(
            [
                {
                    "text": f"Methods for experiment {paper}",
                    "label": "KEEP",
                    "document_id": f"p{paper}",
                },
                {
                    "text": f"Results for experiment {paper}",
                    "label": "KEEP",
                    "document_id": f"p{paper}",
                },
                {
                    "text": f"Page {paper + 1}",
                    "label": "SKIP",
                    "document_id": f"p{paper}",
                },
                {
                    "text": f"Copyright publisher {paper}",
                    "label": "SKIP",
                    "document_id": f"p{paper}",
                },
            ]
        )
    path = tmp_path / "benchmark.csv"
    pd.DataFrame(rows).to_csv(path, index=False)

    result = benchmark_csv(path, test_size=0.25)
    assert result.split == "document-grouped"
    assert result.train_rows + result.test_rows == len(rows)
    assert 0.0 <= result.f1_keep <= 1.0
