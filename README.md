# School Climate Hub

An open infrastructure for understanding climate exposure at the level of individual schools — and turning that understanding into operational tools that protect children's health.

> **Status:** Prototype, May 2026.
> Built as a working submission to the [UNICEF Venture Fund — Funding Frontier Climate Tech for Children's Health](https://www.unicefinnovationfund.org/) call.
> Founding deployment: 50 PSSP/PSRP schools (~12,000 children) operated by [PDLC](https://premierdlc.com) in Gujranwala, Pakistan.

## What's in here

Three modules, each independently useful, designed to work together:

| Module | What it does | Status |
|---|---|---|
| **Climate Vulnerability Dashboard** | Per-school heat, air-quality, flood, and rainfall exposure scores using open satellite + reanalysis data. EMIS-keyed. | Prototype |
| **Parent Advisory Engine** | Template-driven, multilingual (English / Urdu / Punjabi) advisory text generator triggered by daily forecasts. Stubbed SMS/WhatsApp sink. | Prototype |
| **Open School-Climate Data Layer** | The headline open-source artefact: a clean, school-level, EMIS-keyed climate exposure dataset other operators can build models against. Daily refresh. | Schema |

## Why this exists

Climate impacts on schoolchildren — heatwaves cutting attendance, smog episodes triggering respiratory illness, monsoon flooding closing schools for weeks — are usually discussed at the district or provincial level. The school-level data needed to act doesn't exist as a clean, open, machine-readable dataset.

We're building it. Starting with 50 schools. Designed to scale.

## Data sources (all open / free)

- [ERA5](https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5) — temperature, rainfall, humidity (ECMWF Copernicus)
- [MODIS LST](https://modis.gsfc.nasa.gov/data/dataprod/mod11.php) — land-surface temperature (NASA)
- [Sentinel-5P](https://sentinels.copernicus.eu/web/sentinel/missions/sentinel-5p) — NO₂, aerosol, ozone (ESA)
- [CAMS Atmosphere](https://atmosphere.copernicus.eu/) — PM2.5 / air-quality reanalysis (Copernicus)
- [GloFAS](https://www.globalfloods.eu/) — flood risk and return periods (Copernicus)
- [WorldPop](https://www.worldpop.org/) — population reference layer

## Quickstart (planned)

```bash
git clone https://github.com/school-climate-hub/school-climate-hub.git
cd school-climate-hub
make setup           # Python + Node + pre-commit
make ingest          # pulls latest climate data for all schools
make score           # computes vulnerability scores
make dashboard       # starts the dashboard locally
```

> **Note:** the Make targets above are aspirational — the scaffold is in place but the implementations are still being written. See `docs/architecture.md`.

## Repository layout

```
school-climate-hub/
├── data/schools/          School roster (EMIS, coordinates, enrolment)
├── ingestion/             One module per upstream climate source
├── scoring/               Per-school vulnerability + child-burden scoring
├── open_data_layer/       Schema and export pipeline for the public dataset
├── advisory/              Parent advisory content engine
├── dashboard/             Next.js front-end (planned)
├── mockups/               Design mockups (interactive HTML)
└── docs/                  Architecture, data sources, deployment
```

## License

[Apache-2.0](./LICENSE).
The open dataset is published under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — see `open_data_layer/`.

## Acknowledgements

A joint project of [Premier DLC](https://premierdlc.com) and [Beaconhouse Technology](https://beaconhouse.tech).
Submission target: 17 May 2026 — [UNICEF Venture Fund — Funding Frontier Climate Tech for Children's Health](https://www.unicefinnovationfund.org/).
