import subprocess
import sys
from pathlib import Path

import pandas as pd


def test_benchmark_cli_writes_json(tmp_path: Path):
    rows = []
    for index in range(20):
        rows.append({"text": f"Methods result {index}", "label": "KEEP"})
        rows.append({"text": f"Page {index}", "label": "SKIP"})
    csv_path = tmp_path / "labels.csv"
    json_path = tmp_path / "benchmark.json"
    pd.DataFrame(rows).to_csv(csv_path, index=False)

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "cleanlisten.cli",
            "benchmark",
            str(csv_path),
            "--json",
            str(json_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "KEEP F1" in completed.stdout
    assert json_path.exists()
