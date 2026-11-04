"""Unsupervised multi-sensor anomaly ranking for ForestWatch AI.

This module ranks unusual satellite-evidence patterns. It does not classify
illegal activity, estimate a probability of deforestation, or replace field
verification.
"""
from __future__ import annotations

from collections import defaultdict
from typing import Any, Iterable, Mapping

import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


FEATURE_COLUMNS = (
    "ndvi_drop_2024",
    "ndvi_drop_2025",
    "ndvi_change_2025_vs_2024",
    "vv_change_db",
    "vh_change_db",
    "radar_support_flag",
    "radar_observation_available",
)


def _properties(record: Mapping[str, Any]) -> Mapping[str, Any]:
    nested = record.get("properties")
    return nested if isinstance(nested, Mapping) else record


def _matrix_from_records(
    records: Iterable[Mapping[str, Any]],
    feature_names: tuple[str, ...],
) -> tuple[np.ndarray, list[Mapping[str, Any]]]:
    rows: list[list[float]] = []
    properties_list: list[Mapping[str, Any]] = []

    for record in records:
        if not isinstance(record, Mapping):
            continue
        properties = _properties(record)
        try:
            values = [float(properties[name]) for name in feature_names]
        except (KeyError, TypeError, ValueError):
            continue
        if not np.all(np.isfinite(values)):
            continue
        rows.append(values)
        properties_list.append(properties)

    if not rows:
        raise ValueError("No records contain a complete, finite feature vector.")

    return np.asarray(rows, dtype=np.float64), properties_list


def fit_reference_model(
    reference_records: Iterable[Mapping[str, Any]],
    *,
    feature_names: tuple[str, ...] = FEATURE_COLUMNS,
    contamination: float = 0.05,
    random_state: int = 42,
) -> dict[str, Any]:
    """Fit a reproducible Isolation Forest on a random AOI reference sample."""
    if not 0.0 < contamination <= 0.5:
        raise ValueError("contamination must be greater than 0 and at most 0.5.")
    if len(set(feature_names)) != len(feature_names) or not feature_names:
        raise ValueError("feature_names must be a non-empty sequence of unique names.")

    matrix, _ = _matrix_from_records(reference_records, feature_names)
    if matrix.shape[0] < 100:
        raise ValueError(
            f"At least 100 valid reference samples are required; got {matrix.shape[0]}."
        )

    training_matrix, calibration_matrix = train_test_split(
        matrix,
        test_size=0.25,
        random_state=random_state,
        shuffle=True,
    )
    model = make_pipeline(
        StandardScaler(),
        IsolationForest(
            n_estimators=300,
            max_samples=min(512, training_matrix.shape[0]),
            contamination=contamination,
            random_state=random_state,
            n_jobs=-1,
        ),
    )
    model.fit(training_matrix)

    # Calibrate against held-out reference pixels that were not used to fit
    # the scaler or Isolation Forest. Scores remain relative, not probabilities.
    calibration_anomaly = -model.decision_function(calibration_matrix)
    return {
        "model": model,
        "calibration_anomaly_sorted": np.sort(calibration_anomaly),
        "feature_names": tuple(feature_names),
        "reference_sample_count": int(matrix.shape[0]),
        "training_sample_count": int(training_matrix.shape[0]),
        "calibration_sample_count": int(calibration_matrix.shape[0]),
        "contamination_setting": float(contamination),
    }


def score_region_samples(
    reference_model: Mapping[str, Any],
    candidate_records: Iterable[Mapping[str, Any]],
) -> dict[str, dict[str, float | int]]:
    """Aggregate candidate-pixel anomaly percentiles by region ID."""
    feature_names = tuple(reference_model["feature_names"])
    matrix, properties_list = _matrix_from_records(candidate_records, feature_names)

    region_ids: list[str] = []
    keep_indices: list[int] = []
    for index, properties in enumerate(properties_list):
        region_id = properties.get("region_id")
        if region_id is None or str(region_id).strip() == "":
            continue
        region_ids.append(str(region_id))
        keep_indices.append(index)

    if not keep_indices:
        raise ValueError("Candidate samples do not contain region_id properties.")

    matrix = matrix[keep_indices]
    raw_anomaly = -reference_model["model"].decision_function(matrix)
    reference_sorted = np.asarray(reference_model["calibration_anomaly_sorted"])
    percentiles = (
        np.searchsorted(reference_sorted, raw_anomaly, side="right")
        * 100.0
        / reference_sorted.size
    )

    grouped: dict[str, list[float]] = defaultdict(list)
    for region_id, percentile in zip(region_ids, percentiles):
        grouped[region_id].append(float(percentile))

    results: dict[str, dict[str, float | int]] = {}
    for region_id, values in grouped.items():
        scores = np.asarray(values, dtype=np.float64)
        results[region_id] = {
            "ml_anomaly_percentile_median": round(float(np.median(scores)), 3),
            "ml_anomaly_p95_share": round(float(np.mean(scores >= 95.0)), 4),
            "ml_sample_count": int(scores.size),
        }

    return results
