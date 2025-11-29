import unittest
import pandas as pd
from src.cli.split import split_into_dimensions

class TestSplit(unittest.TestCase):
    def setUp(self):
        # Create sample merged dataframe for testing
        self.merged_df = pd.DataFrame({
            'numero_boletim': ['B001', 'B002'],
            'data': ['2023-01-01', '2023-01-02'],
            'desc_tipo_acidente': ['Tipo1', 'Tipo2'],
            'pavimento': ['Asfalto', 'Concreto'],
            'desc_tempo': ['Chuvoso', 'Limpo'],
            'tipo_logradouro': ['Rua', 'Avenida'],
            'nome_logradouro': ['Teste1', 'Teste2'],
            'nome_bairro': ['Bairro1', 'Bairro2'],
            'desc_regional': ['Norte', 'Sul'],
            'coordenada_x': [1.0, 2.0],
            'coordenada_y': [1.0, 2.0],
            'cinto_seguranca': ['Sim', 'Não'],
            'embreagues': ['Não', 'Sim']
        })

    def test_split_into_dimensions(self):
        # Split the merged dataframe
        tables = split_into_dimensions(self.merged_df)
        
        # Check if all expected tables are present
        expected_tables = ['dim_boletim', 'dim_logradouro', 'dim_contexto', 'fato_acidente']
        self.assertTrue(all(table in tables for table in expected_tables))
        
        # Check Dim_Boletim
        boletim = tables['dim_boletim']
        self.assertTrue('pk_boletim' in boletim.columns)
        self.assertTrue('numero' in boletim.columns)
        self.assertEqual(len(boletim), 2)
        
        # Check Dim_Logradouro
        logradouro = tables['dim_logradouro']
        self.assertTrue('pk_logradouro' in logradouro.columns)
        self.assertTrue('tipo' in logradouro.columns)
        self.assertTrue('nome' in logradouro.columns)
        
        # Check Dim_Contexto
        contexto = tables['dim_contexto']
        self.assertTrue('pk_contexto' in contexto.columns)
        self.assertTrue('descricao_tipo' in contexto.columns)
        
        # Check Fato_Acidente
        fato = tables['fato_acidente']
        self.assertTrue('pk_acidente' in fato.columns)
        self.assertTrue('fk_boletim' in fato.columns)
        self.assertTrue('fk_logradouro' in fato.columns)
        self.assertTrue('fk_contexto' in fato.columns)

if __name__ == '__main__':
    unittest.main()