# Reproducible Research Preregistration

A Python project for planning, executing, testing, and documenting
reproducible statistical research.

## Project Structure

- `preregistration/` — research question and analysis plan
- `data/raw/` — original input data
- `data/interim/` — intermediate data
- `data/processed/` — analysis-ready data
- `data/synthetic/` — synthetic datasets for testing
- `src/` — analysis code
- `tests/` — automated tests
- `reports/` — analysis reports and figures
- `evidence/` — execution logs and reproducibility evidence
- `notebooks/` — exploratory notebooks

## Environment

Python 3.12 is recommended for the pinned dependencies.

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run automated tests:

```powershell
python -m pytest -v
```

## Reproducibility

The project pins dependency versions and is designed to separate
the preregistered analysis plan from the code and research results.

No real research findings should be reported until the research
question, data, and analysis plan have been specified.
