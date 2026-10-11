"""Reproducible statistical analysis for synthetic research data."""

from pathlib import Path
import json

import numpy as np
import pandas as pd
from scipy import stats


def generate_synthetic_data(seed: int = 42, n: int = 200) -> pd.DataFrame:
    """Generate reproducible synthetic data for testing the pipeline."""
    if n < 2:
        raise ValueError("n must be at least 2")

    rng = np.random.default_rng(seed)
    group = np.repeat(["control", "treatment"], n // 2)
    if n % 2:
        group = np.append(group, "control")

    outcome = rng.normal(50, 10, n)
    outcome[group == "treatment"] += 4

    return pd.DataFrame({"group": group, "outcome": outcome})


def analyze_data(data: pd.DataFrame) -> dict:
    """Compare outcomes between control and treatment groups."""
    required = {"group", "outcome"}
    if not required.issubset(data.columns):
        raise ValueError(f"Data must contain columns: {sorted(required)}")

    clean = data.loc[:, ["group", "outcome"]].dropna()
    control = clean.loc[clean["group"] == "control", "outcome"].to_numpy(dtype=float)
    treatment = clean.loc[clean["group"] == "treatment", "outcome"].to_numpy(dtype=float)

    if len(control) < 2 or len(treatment) < 2:
        raise ValueError("Each group must contain at least two valid observations")

    if not np.isfinite(control).all() or not np.isfinite(treatment).all():
        raise ValueError("Outcome values must be finite numbers")

    result = stats.ttest_ind(treatment, control, equal_var=False)

    return {
        "analysis": "Welch's independent-samples t-test",
        "n_control": int(len(control)),
        "n_treatment": int(len(treatment)),
        "mean_control": float(np.mean(control)),
        "mean_treatment": float(np.mean(treatment)),
        "mean_difference_treatment_minus_control": float(
            np.mean(treatment) - np.mean(control)
        ),
        "t_statistic": float(result.statistic),
        "p_value": float(result.pvalue),
        "data_type": "synthetic",
        "interpretation_warning": (
            "Synthetic demonstration only; not evidence of a real-world effect."
        ),
    }


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    output_dir = root / "reports"
    output_dir.mkdir(parents=True, exist_ok=True)

    data = generate_synthetic_data(seed=42, n=200)
    data.to_csv(root / "data" / "synthetic" / "example_data.csv", index=False)

    result = analyze_data(data)
    output_path = output_dir / "analysis_results.json"
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(json.dumps(result, indent=2))
    print(f"\nResults saved to: {output_path}")


if __name__ == "__main__":
    main()
