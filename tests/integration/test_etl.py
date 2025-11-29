import unittest
import psycopg2
import pandas as pd
from src.services.db import PostgresService
from src.cli.load import create_tables, load_dataframe_to_table

class TestETLIntegration(unittest.TestCase):
    def setUp(self):
        # Test database configuration
        self.config = {
            'host': 'localhost',
            'port': 5432,
            'user': 'postgres',
            'password': 'etlpass',
            'dbname': 'etl_db'
        }
        
        # Connect to database
        self.db = PostgresService(self.config)
        self.conn = self.db.connect()
        
        # Create test data
        self.test_df = pd.DataFrame({
            'pk_boletim': [1, 2],
            'numero': ['B001', 'B002'],
            'mes': [1, 1],
            'ano': [2023, 2023],
            'dia': [1, 2]
        })

    def tearDown(self):
        # Clean up test data and close connection
        if self.conn:
            cur = self.conn.cursor()
            cur.execute("DROP TABLE IF EXISTS fato_acidente")
            cur.execute("DROP TABLE IF EXISTS dim_boletim")
            cur.execute("DROP TABLE IF EXISTS dim_logradouro")
            cur.execute("DROP TABLE IF EXISTS dim_contexto")
            self.conn.commit()
            self.db.close()

    def test_table_creation(self):
        # Test creating tables
        create_tables(self.conn)
        
        # Verify tables exist
        cur = self.conn.cursor()
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = [row[0] for row in cur.fetchall()]
        
        expected_tables = ['dim_boletim', 'dim_logradouro', 'dim_contexto', 'fato_acidente']
        for table in expected_tables:
            self.assertIn(table, tables)

    def test_data_loading(self):
        # Create tables first
        create_tables(self.conn)
        
        # Test loading data
        load_dataframe_to_table(self.test_df, 'dim_boletim', self.conn)
        
        # Verify data was loaded
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM dim_boletim")
        count = cur.fetchone()[0]
        self.assertEqual(count, 2)

if __name__ == '__main__':
    unittest.main()