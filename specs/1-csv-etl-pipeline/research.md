# Research & Decision Log: CSV ETL Pipeline

## Decision: Use pandas for ETL
- Rationale: pandas provides robust CSV handling, transformation, and merging capabilities, ideal for tabular accident data.
- Alternatives considered: raw Python CSV, Dask, Spark

## Decision: Use psycopg2 for PostgreSQL
- Rationale: psycopg2 is a mature, widely used PostgreSQL driver for Python, supports bulk inserts and transactions.
- Alternatives considered: SQLAlchemy, asyncpg

## Decision: Auto-detect CSV delimiter
- Rationale: Source files may use comma, semicolon, or tab; auto-detection ensures compatibility and reduces manual errors.
- Alternatives considered: fixed delimiter, user-specified

## Decision: Halt ETL on file error
- Rationale: Ensures data integrity and prevents partial/inconsistent loads.
- Alternatives considered: skip errors, retry

## Decision: Basic logging (start/end/errors)
- Rationale: Satisfies constitution and operational needs without excessive log volume.
- Alternatives considered: verbose logging, progress logs

## Decision: Table normalization and splitting
- Rationale: Improves query performance, supports analytics, and aligns with dimensional modeling best practices.
- Alternatives considered: single wide table, denormalized schema

## Decision: Performance targets
- Rationale: 50,000 records/minute and ≤4 hours full load are achievable with chunked pandas processing and PostgreSQL bulk inserts.
- Alternatives considered: higher/lower targets
