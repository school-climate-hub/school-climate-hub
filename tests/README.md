# Tests

## Python unit tests (`tests/`)

```bash
python3.11 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

What's covered:

- **`scoring/vulnerability.py`** — heat/rain threshold-scoring boundaries
  (amber/red thresholds, monotonicity, 0–100 range, NaN/None handling), the
  `burden()` estimate, `load_schools()` against the real 50-school roster,
  the documented stubs (`sample_modis_at_schools()` is a no-op returning
  NaN; AQ is hardcoded `0` in `compute_scores()`), and the HRES/ENS forecast
  sampling logic (`sample_forecast_at_schools`, `sample_ens_at_schools`) —
  exercised against small synthetic in-memory `xarray.Dataset` objects via
  `monkeypatch`, so no network access, CDS/ECMWF credentials, or real GRIB
  files are required.
- **`ingestion/attendance.py`** — the layout-tolerant SAR-workbook parser
  (header-row/EMIS-column detection, month-column detection, out-of-range
  value filtering, fuzzy year-sheet matching), the anonymisation default
  (`school_id_NN` vs `--reveal-emis`), missing-school handling, and the
  aggregate statistics (annual mean, pp-change, lost child-school-days,
  cluster averages). All of this runs against a tiny **synthetic** workbook
  built with `openpyxl` in `tests/conftest.py` (3 fake schools, fake EMIS
  codes starting `9000000x`) — no real Premier DLC data or PII is used.

Explicitly **not** unit-tested (network/credentials-dependent, no mocking
attempted): `ingestion/era5.py` (Copernicus CDS API) and the network-facing
parts of `ingestion/ecmwf_forecast.py` (`latest_cycle()`, `fetch_hres()`,
`fetch_ens()` — these hit the ECMWF S3 mirror). The pure step-planning logic
in `ecmwf_forecast.hres_steps()` and the `ENS_STEPS` constant have no
dedicated tests either but are trivial (static lists).

## E2E smoke tests (`e2e/`)

Playwright project that serves the static site locally
(`python3 -m http.server`, no build step) and drives a real Chromium browser
against it.

```bash
cd e2e
npm install
npx playwright install --with-deps chromium   # one-time browser download
npm test
```

Covers: the operator console (`index.html`) loads with no console/page
errors, the Leaflet map container renders, the primary nav views (Overview /
Schools / Data / About / Settings) are present and switchable, the schools
table populates from `schools.json`/`scores.json` (50 rows), and the chat
panel opens/closes without triggering a network call.

## CI

`.github/workflows/ci.yml` runs three jobs on every push/PR: `ruff check`
(scoped to `scoring/`, `ingestion/`, `tests/`), `pytest` on Python 3.11, and
the Playwright smoke suite (installs Chromium via
`npx playwright install --with-deps`).
