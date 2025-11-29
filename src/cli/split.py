from extract import extract_csv_files
from transform import merge_and_transform_data
import pandas as pd

def split_into_dimensions(df: pd.DataFrame):
    boletim_df = create_boletim_dimension(df)
    logradouro_df = create_logradouro_dimension(df)
    contexto_df = create_contexto_dimension(df)
    fato_df = create_fato_acidente(df, boletim_df, logradouro_df, contexto_df)
    
    return {
        'dim_boletim': boletim_df,
        'dim_logradouro': logradouro_df,
        'dim_contexto': contexto_df,
        'fato_acidente': fato_df
    }

def create_boletim_dimension(df: pd.DataFrame):
    boletim_df = pd.DataFrame()
    
    boletim_df['pk_boletim'] = range(1, len(df) + 1)
    
    boletim_df['numero'] = df['numero_boletim'].values
   
    boletim_df['data'] = pd.to_datetime(df['data_boletim'].values, format="%d/%m/%Y %H:%M")
    boletim_df['mes'] = boletim_df['data'].dt.month
    boletim_df['ano'] = boletim_df['data'].dt.year
    boletim_df['dia'] = boletim_df['data'].dt.day
    
    boletim_df = boletim_df[['pk_boletim', 'numero', 'mes', 'ano', 'dia']]
    
    return boletim_df

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

def create_contexto_dimension(df: pd.DataFrame):
    #.drop_duplicates(subset=['desc_tipo_acidente', 'pavimento', 'desc_tempo', 'cinto_seguranca', 'embreagues'])
    contexto_df = df.copy()
    contexto_df['pk_contexto'] = range(1, len(contexto_df) + 1)
    
    contexto_df = contexto_df[[
        'pk_contexto',
        'desc_tipo_acidente',
        'pavimento',
        'desc_tempo',
        'cinto_seguranca',
        'embreagues'
    ]]
    contexto_df = contexto_df.rename(columns={
        'desc_tipo_acidente': 'descricao_tipo',
        'desc_tempo': 'tempo_atmosferico'
    })
    
    return contexto_df

def create_fato_acidente(df: pd.DataFrame, boletim_df: pd.DataFrame, logradouro_df: pd.DataFrame, contexto_df: pd.DataFrame):
    fato_df = pd.DataFrame()
    fato_df['pk_acidente'] = range(1, len(df) + 1)
    
    fato_df ['pk_boletim'] = boletim_df[['pk_boletim']]
    fato_df['pk_contexto'] = contexto_df[['pk_contexto']]
    fato_df['pk_logradouro'] = logradouro_df[['pk_logradouro']]

    fato_df.rename(columns={
        'pk_boletim':'fk_boletim',
        'pk_contexto':'fk_contexto',
        'pk_logradouro':'fk_logradouro'
    }, inplace= True)
    
    fato_df['indicador_fatalidade'] = df[['indicador_fatalidade']].replace({'SIM': True, 'NÃO': False})

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