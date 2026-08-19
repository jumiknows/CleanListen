from pathlib import Path

import pandas as pd

from cleanlisten.model import load_model, train_csv


def test_train_csv_accepts_alias_schema(tmp_path: Path):
    frame = pd.DataFrame(
        {
            "line": ["Methods", "Results", "Page 4", "Copyright publisher"] * 3,
            "decision": ["KEEP", "KEEP", "SKIP", "SKIP"] * 3,
        }
    )
    csv_path = tmp_path / "labels.csv"
    model_path = tmp_path / "model.joblib"
    frame.to_csv(csv_path, index=False)

    summary = train_csv(csv_path, model_path)
    model = load_model(model_path)

    assert summary.rows == 12
    assert model_path.exists()
    assert hasattr(model, "predict_proba")
