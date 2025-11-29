import unittest
import pandas as pd
from src.cli.transform import merge_and_transform_data

class TestTransform(unittest.TestCase):
    def setUp(self):
        # Create sample dataframes for testing
        self.df1 = pd.DataFrame({
            'numero_boletim': ['B001', 'B002'],
            'data': ['2023-01-01', '2023-01-02'],
            'desc_tipo_acidente': ['Tipo1', 'Tipo2']
        })
        
        self.df2 = pd.DataFrame({
            'numero_boletim': ['B001', 'B002'],
            'pavimento': ['Asfalto', 'Concreto'],
            'desc_tempo': ['Chuvoso', 'Limpo']
        })

    def test_merge_and_transform(self):
        # Test merging of dataframes
        result = merge_and_transform_data([self.df1, self.df2])
        
        # Check if result contains expected columns
        expected_columns = ['numero_boletim', 'data', 'desc_tipo_acidente', 'pavimento', 'desc_tempo']
        self.assertTrue(all(col in result.columns for col in expected_columns))
        
        # Check if number of rows is correct
        self.assertEqual(len(result), 2)
        
        # Check if merge was correct
        self.assertEqual(result.iloc[0]['numero_boletim'], 'B001')
        self.assertEqual(result.iloc[0]['pavimento'], 'Asfalto')

    def test_empty_dataframes(self):
        # Test handling of empty dataframe list
        with self.assertRaises(ValueError):
            merge_and_transform_data([])

if __name__ == '__main__':
    unittest.main()