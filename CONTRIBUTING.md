# Contributing to School Climate Hub

Thank you for your interest in contributing. School Climate Hub is open infrastructure
for school-level climate-exposure data and operational tools for children's health.

## Ground rules

- By contributing, you agree that your contributions are licensed under the project's
  **Apache License 2.0** (code) and **CC BY 4.0** (data/content).
- **Never commit personally identifiable information (PII).** No parent or child PII is
  held anywhere in this project. School-level data is anonymised by default; do not add
  named rosters, contact details, or health-incident records to the repository.
- Be respectful. This project follows our [Code of Conduct](CODE_OF_CONDUCT.md).

## Project layout

- `ingestion/` — Python 3.11 data ingestion (ERA5 / Copernicus, ECMWF forecasts, attendance)
- `scoring/` — per-school hazard scoring (`vulnerability.py`)
- `dashboard/` / `index.html` — the operator console (static site, Leaflet)
- `worker/` — Cloudflare Worker (TypeScript) for the grounded Claude chat
- `open_data_layer/` — open dataset schema and export
- `docs/` — architecture, PRD, requirements, roadmap

## Development setup

```bash
# Python
python3.11 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# Worker
cd worker && npm install
```

## Running checks locally

```bash
ruff check .            # lint
pytest                  # unit tests
cd e2e && npm test      # Playwright end-to-end tests
```

CI runs the same checks on every push (see `.github/workflows/ci.yml`).

## Making a change

1. Create a branch off `main`.
2. Make your change with a focused commit message (`feat:`, `fix:`, `docs:`, `test:`).
3. Ensure `ruff`, `pytest`, and the e2e suite pass.
4. Open a pull request describing what changed and why.

## Reporting bugs / security issues

Open a GitHub issue for bugs. For security vulnerabilities, follow
[SECURITY.md](SECURITY.md) — do **not** open a public issue.
