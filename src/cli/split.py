from extract import extract_csv_files
from transform import merge_and_transform_data
import pandas as pd

def split_into_dimensions(df: pd.DataFrame):
    tempo_df = create_tempo_dimension(df)
    logradouro_df = create_logradouro_dimension(df)
    pista_df = create_pista_dimension(df)
    motorista_df = create_motorista_dimension(df)
    acidente_df = create_acidente_dimension(df)
    fato_df = create_fato_boletim(df, tempo_df, logradouro_df, pista_df, motorista_df, acidente_df)
    
    return {
        'dim_tempo': tempo_df,
        'dim_logradouro': logradouro_df,
        'dim_pista': pista_df,
        'dim_motorista': motorista_df,
        'dim_acidente': acidente_df,
        'fato_boletim': fato_df
    }

def create_tempo_dimension(df: pd.DataFrame):
    tempo_df = pd.DataFrame()
    
    tempo_df['pk_tempo'] = range(1, len(df) + 1)
       
    tempo_df['data'] = pd.to_datetime(df['data_boletim'].values, format="%d/%m/%Y %H:%M")
    tempo_df['mes'] = tempo_df['data'].dt.month
    tempo_df['ano'] = tempo_df['data'].dt.year
    tempo_df['dia'] = tempo_df['data'].dt.day
    
    tempo_df = tempo_df[['pk_tempo', 'mes', 'ano', 'dia']]
    
    return tempo_df

def create_logradouro_dimension(df: pd.DataFrame):
    #.drop_duplicates(subset=['tipo_logradouro', 'nome_logradouro', 'nome_bairro', 'desc_regional', 'coordenada_x', 'coordenada_y'])
    logradouro_df = df.copy()
    
    logradouro_df['pk_logradouro'] = range(1, len(logradouro_df) + 1)
    
    logradouro_df = logradouro_df[[
        'pk_logradouro',
        'tipo_logradouro',
        'nome_logradouro',
        'nome_bairro',
        'desc_regional',
        'coordenada_x',
        'coordenada_y'
    ]]
    
    logradouro_df.rename(columns={
        'tipo_logradouro': 'tipo',
        'nome_logradouro': 'nome',
        'nome_bairro': 'bairro',
        'desc_regional': 'regiao'
    }, inplace= True)
    
    return logradouro_df

def create_pista_dimension(df: pd.DataFrame):
    #.drop_duplicates(subset=['desc_tipo_acidente', 'pavimento', 'desc_tempo', 'cinto_seguranca', 'embreagues'])
    pista_df = df.copy()
    pista_df['pk_pista'] = range(1, len(pista_df) + 1)
    
    pista_df = pista_df[[
        'pk_pista',
        'pavimento',
        'desc_tempo',
    ]]
    pista_df = pista_df.rename(columns={
        'desc_tempo': 'tempo_atmosferico'
    })
    
    return pista_df

def create_motorista_dimension(df: pd.DataFrame):
    #.drop_duplicates(subset=['desc_tipo_acidente', 'pavimento', 'desc_tempo', 'cinto_seguranca', 'embreagues'])
    motorista_df = df.copy()
    motorista_df['pk_motorista'] = range(1, len(motorista_df) + 1)
    
    motorista_df = motorista_df[[
        'pk_motorista',
        'cinto_seguranca',
        'embreagues'
    ]]
    
    return motorista_df

def create_acidente_dimension(df: pd.DataFrame):
    #.drop_duplicates(subset=['desc_tipo_acidente', 'pavimento', 'desc_tempo', 'cinto_seguranca', 'embreagues'])
    acidente_df = df.copy()
    acidente_df['pk_acidente'] = range(1, len(acidente_df) + 1)
    
    acidente_df = acidente_df[[
        'pk_acidente',
        'desc_tipo_acidente',
    ]]

    acidente_df['indicador_fatalidade'] = df[['indicador_fatalidade']].replace({'SIM': True, 'NÃO': False})
    acidente_df = acidente_df.rename(columns={
        'desc_tipo_acidente': 'descricao_tipo',
    })
    
    return acidente_df

def create_fato_boletim(df: pd.DataFrame, boletim_df: pd.DataFrame, logradouro_df: pd.DataFrame, pista_df: pd.DataFrame, motorista_df: pd.DataFrame, acidente_df: pd.DataFrame):
    fato_df = pd.DataFrame()
    fato_df['pk_boletim'] = range(1, len(df) + 1)

    fato_df['numero_identificacao'] = df['numero_boletim'].values
    
    fato_df ['pk_tempo'] = boletim_df[['pk_tempo']]
    fato_df['pk_pista'] = pista_df[['pk_pista']]
    fato_df['pk_motorista'] = motorista_df[['pk_motorista']]
    fato_df['pk_acidente'] = acidente_df[['pk_acidente']]
    fato_df['pk_logradouro'] = logradouro_df[['pk_logradouro']]

    fato_df.rename(columns={
        'pk_tempo':'fk_tempo',
        'pk_pista':'fk_contexto',
        'pk_motorista':'fk_motorista',
        'pk_acidente':'fk_acidente',
        'pk_logradouro':'fk_logradouro'
    }, inplace= True)
    
    # # for line in fato_df.iterrows():
    # fato_df['quantidade_vitimas'] = 1  # Placeholder - adjust based on actual data
    # fato_df['numero_envolvidos'] = 1  # Placeholder - adjust based on actual data

    return fato_df

if __name__ == "__main__":
    dataframes = extract_csv_files()
    merged_data = merge_and_transform_data(dataframes)
    
    tables = split_into_dimensions(merged_data)
    
    for table_name, df in tables.items():
        print(f"\n{table_name} shape: {df.shape}")
        print("Columns:", df.columns.tolist())