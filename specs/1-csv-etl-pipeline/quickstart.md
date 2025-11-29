# Quickstart: CSV ETL Pipeline

## Prerequisites
- Python 3.11
- Install dependencies: `pip install pandas psycopg2`
- Docker installed
- PostgreSQL container (official image) with a dedicated volume for data

## Steps
1. Place CSV files in the `data/` subdirectories
2. Start PostgreSQL using Docker:
   ```bash
   docker run --name etl-postgres -e POSTGRES_PASSWORD=etlpass -p 5432:5432 -v etl_pgdata:/var/lib/postgresql/data -d postgres:latest
   ```
   - This creates a new container with a dedicated volume `etl_pgdata` for persistent storage.
3. Configure column specifications and database connection (use `localhost:5432`, user `postgres`, password `etlpass`).
4. Run the ETL script:
   - Extract tables from CSVs using pandas
   - Merge rows by `numero_boletim`, keep specified columns
   - Split unified table into Dim_Boletim, Dim_Logradouro, Fato_Acidente, Dim_Contexto
   - Create tables in PostgreSQL and load data
5. Check logs for start/end/errors
6. Validate loaded data in PostgreSQL

## Example Command
```bash
python src/cli/run_etl.py --config config.yaml
```
