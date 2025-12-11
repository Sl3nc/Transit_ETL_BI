import pandas as pd
from yaml import safe_load
from pathlib import Path

def config_input() -> Path:
    with open('config.yaml', 'r') as f:
        return Path(__file__).parent.parent.parent / safe_load(f).get('input_dir', 'data')

def extract_csv_files():
    dataframes = []
    data_dir = config_input()
    for subdir in data_dir.iterdir():
        for file in subdir.iterdir():
            if file.match('*.csv'):
                df = pd.read_csv(
                    file, 
                    encoding='latin1', 
                    delimiter=';',
                    skipinitialspace=True,
                    on_bad_lines='skip',
                )
                
                df.columns = df.columns.str.lower()
                dataframes.append(df)
                            
    return dataframes

if __name__ == "__main__":
    dataframes = extract_csv_files()
    print(f"Successfully extracted {len(dataframes)} CSV files")