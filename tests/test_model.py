from cleanlisten.model import build_pipeline, keep_lines, predict_lines


def trained_model():
    texts = [
        "Methods and experimental setup",
        "The results show a significant improvement in recall.",
        "Discussion and limitations",
        "Page 12",
        "Copyright 2026 Example Publisher",
        "https://doi.org/10.1000/example",
    ]
    labels = [1, 1, 1, 0, 0, 0]
    model = build_pipeline()
    model.fit(texts, labels)
    return model, texts


def test_pipeline_filters_obvious_noise():
    model, texts = trained_model()
    cleaned = keep_lines(texts, model, threshold=0.5)
    assert "Discussion and limitations" in cleaned
    assert "Page 12" not in cleaned


def test_prediction_contains_probability():
    model, _ = trained_model()
    prediction = predict_lines(["Results and discussion"], model)[0]
    assert 0.0 <= prediction.keep_probability <= 1.0
    assert isinstance(prediction.keep, bool)
