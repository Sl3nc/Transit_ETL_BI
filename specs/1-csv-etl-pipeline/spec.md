# CSV ETL Pipeline Specification

## Overview

This feature implements an ETL (Extract, Transform, Load) pipeline that processes CSV files from the data directory, performs column selection based on specifications, and loads the transformed data into a database.

## Clarifications

### Session 2025-10-27
- Q: What are the specific performance targets for ETL processing? → A: Process 50k records/minute, complete full load within 4 hours
- Q: What should be the error recovery strategy? → A: Stop entire process on any file error
- Q: How should CSV file delimiters be handled? → A: Auto-detect delimiter per file
- Q: How should database tables be named? → A: Use category only (e.g., pessoas)
- Q: What level of logging detail is required? → A: Basic: Start/end events and errors only

## User Scenarios & Testing

### Scenario 1: Basic ETL Process
1. System reads CSV files from the "data" directory
2. System identifies and retains only the specified columns
3. System loads the transformed data into the target database
4. User can verify the successful data loading

### Scenario 2: Error Handling
1. System detects missing or malformed CSV files
2. System validates column specifications against actual CSV structure
3. System reports any issues during the ETL process
4. User receives clear error messages for troubleshooting

## Functional Requirements

1. CSV Data Extraction
   - System MUST read all CSV files from the following subdirectories:
     - data/logradouros
     - data/ocorrencias
     - data/pessoas
     - data/veiculos
   - System MUST validate CSV file encoding and structure
   - System MUST handle large CSV files efficiently

2. Data Transformation
   - System MUST identify available columns in each CSV file
   - System MUST filter columns based on provided specifications
   - System MUST maintain data types integrity during transformation
   - System MUST handle missing or null values appropriately

3. Data Loading
   - System MUST establish connection to the target database
   - System MUST create appropriate database tables if they don't exist
   - System MUST load transformed data into the database
   - System MUST maintain data consistency during loading

4. Error Handling & Logging
   - System MUST validate input files before processing
   - System MUST log the following events with timestamps:
     * ETL process start
     * Each file processing start/end
     * Any errors or failures
     * ETL process completion
   - System MUST provide detailed error messages for failures
   - System MUST support transaction rollback on failures
   - System MUST halt the entire ETL process immediately upon encountering any file error
   - System MUST preserve the error state and details for investigation
   - System MUST ensure no partial data is committed to the database when an error occurs

### Column Specifications
The system will maintain specific columns for each file type. Column specifications will be provided as configuration for each file category.

### Database Configuration
The system will use PostgreSQL as the target database system, leveraging its robust support for large datasets and complex queries.

### Data Type Handling
The system will use automatic type inference to determine appropriate data types for each column during the database table creation. This includes:
- Automatic detection of numeric fields
- Date/time format recognition
- Text field sizing optimization
- Boolean value detection

## Success Criteria

1. Data Extraction
   - All CSV files are successfully read and validated
   - File encoding issues are detected and reported
   - Large files (>1GB) are processed without memory issues

2. Data Transformation
   - Only specified columns are present in transformed data
   - Data types match between source and target
   - No data loss during transformation (row count matches)

3. Data Loading
   - All transformed data is successfully loaded into database
   - Database schema matches transformed data structure
   - Data integrity is maintained (no duplicates or corrupted records)

4. Performance
   - ETL process MUST process at least 50,000 records per minute
   - Full data load MUST complete within 4 hours
   - Memory usage MUST remain stable during processing
   - Database connection pool MUST be efficiently managed

## Key Entities

### Source Files
- logradouros/*.csv
- ocorrencias/*.csv
- pessoas/*.csv
- veiculos/*.csv

### Database Tables
- Will mirror the structure of transformed CSV data
- Tables MUST be named using the names:
  - Dim_Logradouros
  - Fato_Acidente
  - Dim_Boletim
  - Dim_Contexto
- Multiple CSV files from the same category MUST be merged into their respective category table

## Assumptions

1. CSV files may use different delimiters (system will auto-detect)
2. Common delimiters (comma, semicolon, tab) MUST be supported
3. Files are encoded in a standard format (UTF-8 or similar)
3. Source files contain headers for column identification
4. Basic network connectivity to database is available
5. Sufficient storage space exists in target database

## Limitations & Future Enhancements

1. Initial version may not support:
   - Real-time data processing
   - Incremental updates
   - Custom data transformations
   - Advanced data validation rules

2. Future enhancements could include:
   - Parallel processing of multiple files
   - Custom column mappings
   - Data quality scoring
   - Automated schema evolution