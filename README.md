# ETL Pipeline Documentation

## Overview
This ETL pipeline processes traffic accident data from CSV files and loads it into a normalized PostgreSQL database. The pipeline follows a modular architecture with distinct extract, transform, load phases.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start PostgreSQL using Docker:
   ```bash
   docker-compose up -d
   ```

3. Configure the pipeline:
   - Update `config.yaml` with database connection details
   - Verify column specifications in `config.yaml`

## Directory Structure
```
src/
├── cli/
│   ├── extract.py  - CSV data extraction
│   ├── transform.py - Data merging and transformation
│   ├── split.py    - Data normalization
│   └── load.py     - PostgreSQL loading
├── models/         - Data models
└── services/       - Database service
```

## Usage
Run the complete ETL pipeline:
```bash
python src/cli/load.py
```

Or run individual phases:
```bash
python src/cli/extract.py  # Test extraction
python src/cli/transform.py  # Test transformation
python src/cli/split.py  # Test splitting
```

## Data Model
1. Dim_Boletim (Report Dimension)
   - Primary key and report number
   - Date components (year, month, day)

2. Dim_Logradouro (Location Dimension)
   - Address details
   - Geographical coordinates
   - Region information

3. Dim_Contexto (Context Dimension)
   - Accident type
   - Road and weather conditions
   - Safety factors

4. Fato_Acidente (Accident Facts)
   - Foreign keys to dimensions
   - Accident metrics

## Error Handling
- CSV encoding auto-detection
- Delimiter auto-detection
- Transaction rollback on failure
- Detailed error logging

## Performance
- Batch processing for database loads
- Memory-efficient data processing
- Connection pooling

## Dependencies
- pandas: Data processing
- psycopg2: PostgreSQL connectivity
- PyYAML: Configuration management
- Docker: Database containerization