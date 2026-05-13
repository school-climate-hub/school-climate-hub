"""Climate data ingestion pipelines.

Each module ingests one upstream source and writes parquet to data/raw/.
The orchestrator (run.py) calls them and merges into the warehouse.
"""
