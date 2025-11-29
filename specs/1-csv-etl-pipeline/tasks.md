# Task Checklist: CSV ETL Pipeline

## Phase 1: Setup
- [ ] T001 Create project structure per implementation plan
- [ ] T002 Initialize Python environment and install dependencies in requirements.txt
- [ ] T003 [P] Create Docker setup for PostgreSQL with dedicated volume (docker-compose.yml)
- [ ] T004 [P] Create config.yaml for column specifications and DB connection

## Phase 2: Foundational
- [ ] T005 [P] Create src/models/boletim.py for Dim_Boletim entity
- [ ] T006 [P] Create src/models/logradouro.py for Dim_Logradouro entity
- [ ] T007 [P] Create src/models/contexto.py for Dim_Contexto entity
- [ ] T008 [P] Create src/models/acidente.py for Fato_Acidente entity
- [ ] T009 [P] Create src/services/db.py for PostgreSQL connection and table creation

## Phase 3: User Story 1 (Extract, Transform, Merge)
- [ ] T010 [US1] Implement CSV extraction logic in src/cli/extract.py
- [ ] T011 [US1] Implement row merging by numero_boletim in src/cli/transform.py
- [ ] T012 [US1] Filter and retain specified columns in src/cli/transform.py
- [ ] T013 [US1] Validate merged data and log results in src/cli/transform.py

## Phase 4: User Story 2 (Split & Normalize)
- [ ] T014 [US2] Split unified table into Dim_Boletim, Dim_Logradouro, Fato_Acidente, Dim_Contexto in src/cli/split.py
- [ ] T015 [US2] Map columns to normalized tables in src/cli/split.py
- [ ] T016 [US2] Validate normalized tables and log results in src/cli/split.py

## Phase 5: User Story 3 (Load to PostgreSQL)
- [ ] T017 [US3] Implement data loading logic for all tables in src/cli/load.py
- [ ] T018 [US3] Ensure transaction rollback on error in src/cli/load.py
- [ ] T019 [US3] Log start/end/errors for ETL process in src/cli/load.py
- [ ] T020 [US3] Validate loaded data in PostgreSQL

## Final Phase: Polish & Cross-Cutting Concerns
- [ ] T021 Add README.md and update quickstart.md
- [ ] T022 [P] Add integration tests for ETL pipeline in tests/integration/test_etl.py
- [ ] T023 [P] Add unit tests for transformation logic in tests/unit/test_transform.py
- [ ] T024 [P] Add contract tests for API in tests/contract/test_api.py

## Dependencies
- Setup and foundational phases must be completed before user stories
- User stories are sequential: US1 → US2 → US3
- Polish phase can be executed in parallel after user stories

## Parallel Execution Examples
- T003 (Docker setup) and T004 (config) can run in parallel
- Entity model tasks (T005-T008) can run in parallel
- Test tasks (T022-T024) can run in parallel after implementation

## Implementation Strategy
- MVP: Complete User Story 1 (Extract, Transform, Merge)
- Incremental delivery: Add normalization, then loading, then tests and polish
