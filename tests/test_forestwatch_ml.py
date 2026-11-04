import numpy as np
import pytest

from forestwatch_ml import (
    FEATURE_COLUMNS,
    fit_reference_model,
    score_region_samples,
)


def _record(region_id, values):
    return {
        "properties": {
            "region_id": region_id,
            **dict(zip(FEATURE_COLUMNS, values)),
        }
    }


def test_isolation_forest_scores_candidate_region_samples():
    rng = np.random.default_rng(17)
    reference = [
        _record("reference", row)
        for row in rng.normal(0.0, 0.12, size=(500, len(FEATURE_COLUMNS)))
    ]
    model = fit_reference_model(reference)

    normal = rng.normal(0.0, 0.12, size=(20, len(FEATURE_COLUMNS)))
    clearing_like = np.tile(
        np.array([0.65, 0.62, -0.03, 1.2, -2.8, 1.0, 1.0]),
        (20, 1),
    )
    candidates = [
        _record("normal-region", row) for row in normal
    ] + [
        _record("anomalous-region", row) for row in clearing_like
    ]

    scores = score_region_samples(model, candidates)

    assert set(scores) == {"normal-region", "anomalous-region"}
    assert scores["anomalous-region"]["ml_sample_count"] == 20
    assert scores["anomalous-region"]["ml_anomaly_percentile_median"] > (
        scores["normal-region"]["ml_anomaly_percentile_median"]
    )
    assert 0.0 <= scores["anomalous-region"]["ml_anomaly_p95_share"] <= 1.0


def test_model_rejects_too_few_reference_samples():
    records = [
        _record("reference", np.zeros(len(FEATURE_COLUMNS)))
        for _ in range(99)
    ]
    with pytest.raises(ValueError, match="At least 100"):
        fit_reference_model(records)


def test_model_drops_incomplete_or_non_finite_records():
    rng = np.random.default_rng(4)
    reference = [
        _record("reference", row)
        for row in rng.normal(0.0, 0.1, size=(150, len(FEATURE_COLUMNS)))
    ]
    model = fit_reference_model(reference)
    candidate = [
        _record("region-a", np.zeros(len(FEATURE_COLUMNS))),
        {"properties": {"region_id": "region-a", "ndvi_drop_2024": float("nan")}},
    ]

    scores = score_region_samples(model, candidate)
    assert scores["region-a"]["ml_sample_count"] == 1
