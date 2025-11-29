# Data Model: CSV ETL Pipeline

## Entities & Tables

### Dim_Boletim
- pk_boletim (primary key)
- numero
- mes
- ano
- dia

### Dim_Logradouro
- pk_logradouro (primary key)
- tipo
- nome
- bairro
- regiao
- coordenada_x
- coordenada_y

### Fato_Acidente
- pk_acidente (primary key)
- fk_boletim (foreign key to Dim_Boletim)
- fk_contexto (foreign key to Dim_Contexto)
- fk_logradouro (foreign key to Dim_Logradouro)
- quantidade_vitimas
- indicador_fatalidade
- numero_envolvidos

### Dim_Contexto
- pk_contexto (primary key)
- descricao_tipo
- pavimento
- tempo_atmosferico
- cinto_seguranca
- embriagues

## Relationships
- Fato_Acidente references Dim_Boletim, Dim_Contexto, and Dim_Logradouro via foreign keys
- Dim_Boletim, Dim_Logradouro, and Dim_Contexto are dimension tables for analytics

## Validation Rules
- All primary keys must be unique
- Foreign keys must reference existing dimension records
- Data types inferred automatically (int, float, text, date)
- Null values handled per table specification
