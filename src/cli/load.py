from extract import extract_csv_files
from transform import merge_and_transform_data
from split import split_into_dimensions
from yaml import safe_load
from pathlib import Path

def config_output() -> dict:
    with open('config.yaml', 'r') as f:
        return safe_load(f).get('output_dir', 'output')

def save_tables_to_csv(tables, output_dir='output'):
    root = Path(__file__).parent.parent.parent
    root = root.joinpath(output_dir)
    root.mkdir(exist_ok=True)

    for table_name, df in tables.items():
        path = root.joinpath(f"{table_name}.csv")
        df.to_csv(path, index=False, encoding='utf-8')

if __name__ == "__main__":
    print("Extracting data from CSV files...")
    dataframes = extract_csv_files()
    
    print("Merging and transforming data...")
    merged_data = merge_and_transform_data(dataframes)
    
    print("Splitting data into dimension tables...")
    tables = split_into_dimensions(merged_data)
    
    output_dir = config_output()
    print(f"\nSaving tables to CSV in '{output_dir}'...")
    save_tables_to_csv(tables, output_dir=output_dir)