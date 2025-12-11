from extract import extract_csv_files
import pandas as pd
import yaml

def columns_keep():
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)['columns']['keep']

def merge_and_transform_data(dataframes: list[pd.DataFrame]) -> pd.DataFrame:
    if not dataframes: raise ValueError("No dataframes provided for merging")
    
    columns_to_keep = columns_keep()
    processed_dfs = []
    
    column_mappings = {
        'num_boletim': 'numero_boletim',
        'nº_boletim': 'numero_boletim',
        'n§_boletim': 'numero_boletim',
        'data hora_boletim': 'data_boletim',
        'data_hora_boletim': 'data_boletim',
    }
    
    for df in dataframes:
        processed_df = df.copy()
        
        for wrong, right in column_mappings.items():
            if wrong in df.columns:
                processed_df.rename(columns={wrong: right}, inplace=True)
        
        if 'numero_boletim' in processed_df.columns:
            processed_df['numero_boletim'] = processed_df['numero_boletim'].astype(str)
            
        available_columns = [
            col for col in processed_df.columns if col in columns_to_keep
        ]

        if available_columns:
            processed_df.drop_duplicates('numero_boletim', inplace=True, ignore_index=True)
            processed_dfs.append(processed_df[available_columns])
    
    return merge_df(processed_dfs)

def merge_df(processed_dfs):
    merged_df = processed_dfs[0]
    for df in processed_dfs[1:]:
        merged_df = pd.merge(
            merged_df, df, on='numero_boletim', how='outer', suffixes=('_left', '_right')
        )

        for col in merged_df.columns:
            if col.endswith('_left'):
                base_col = col[:-5] 
                right_col = base_col + '_right'

                if right_col in merged_df.columns:
                    merged_df[base_col] = merged_df[col].combine_first(merged_df[right_col])
                    merged_df.drop(columns=[col, right_col], inplace=True)

    merged_df.dropna(how='all', inplace=True)
    return merged_df

if __name__ == "__main__":    
    dataframes = extract_csv_files()
    merged_data = merge_and_transform_data(dataframes)
    print(f"Successfully merged data. Final shape: {merged_data.shape}")