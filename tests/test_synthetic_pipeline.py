import pandas as pd
import pytest

from src.analyze import analyze_data, generate_synthetic_data


def test_synthetic_data_is_reproducible():
    first = generate_synthetic_data(seed=42, n=100)
    second = generate_synthetic_data(seed=42, n=100)
    pd.testing.assert_frame_equal(first, second)


def test_generated_data_has_both_groups():
    data = generate_synthetic_data(seed=42, n=100)
    assert set(data["group"]) == {"control", "treatment"}
    assert len(data) == 100


def test_analysis_returns_expected_fields():
    data = generate_synthetic_data(seed=42, n=100)
    result = analyze_data(data)

    assert result["n_control"] == 50
    assert result["n_treatment"] == 50
    assert 0 <= result["p_value"] <= 1
    assert result["data_type"] == "synthetic"


def test_missing_required_column_is_rejected():
    with pytest.raises(ValueError, match="Data must contain columns"):
        analyze_data(pd.DataFrame({"outcome": [1, 2, 3]}))


def test_groups_need_at_least_two_observations():
    data = pd.DataFrame({
        "group": ["control", "control", "treatment"],
        "outcome": [10, 12, 15],
    })
    with pytest.raises(ValueError, match="at least two"):
        analyze_data(data)


def test_non_finite_values_are_rejected():
    data = pd.DataFrame({
        "group": ["control", "control", "treatment", "treatment"],
        "outcome": [10, 12, float("inf"), 15],
    })
    with pytest.raises(ValueError, match="finite"):
        analyze_data(data)
