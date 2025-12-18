import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.load import load_to_postgres, load_to_csv, load_to_spreadsheet

class TestLoad(unittest.TestCase):

    @patch('utils.load.create_engine')
    def test_load_to_postgres_success(self, mock_create_engine):
        mock_engine = MagicMock()
        mock_connection = MagicMock()
        mock_create_engine.return_value = mock_engine
        mock_engine.connect.return_value.__enter__.return_value = mock_connection
        
        df = pd.DataFrame({'col': [1, 2]})
        db_url = "postgresql://user:pass@localhost:5432/db"
        
        load_to_postgres(df, db_url)
        
        # Verify engine created with correct URL
        mock_create_engine.assert_called_with(db_url)
    
    @patch('pandas.DataFrame.to_sql')
    @patch('utils.load.create_engine')
    def test_load_to_postgres_call_to_sql(self, mock_create_engine, mock_to_sql):
        mock_engine = MagicMock()
        mock_connection = MagicMock()
        mock_create_engine.return_value = mock_engine
        mock_engine.connect.return_value.__enter__.return_value = mock_connection

        df = pd.DataFrame({'col': [1]})
        load_to_postgres(df, "url")
        
        mock_to_sql.assert_called_once()
        args, kwargs = mock_to_sql.call_args
        self.assertEqual(args[0], 'fashion') # Table name
        self.assertEqual(kwargs['if_exists'], 'replace')

    @patch('pandas.DataFrame.to_csv')
    def test_load_to_csv(self, mock_to_csv):
        df = pd.DataFrame({'col': [1]})
        load_to_csv(df, "out.csv")
        
        mock_to_csv.assert_called_once_with("out.csv", index=False)

    @patch('utils.load.credential')
    @patch('utils.load.build')
    @patch('utils.load.RANGE_NAME', 'TEST_RANGE')
    @patch('utils.load.SPREADSHEET_ID', 'TEST_ID')
    def test_load_to_spreadsheet(self, mock_build, mock_credential):
        # Setup mocks
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        mock_sheets = mock_service.spreadsheets.return_value
        mock_values = mock_sheets.values.return_value
        mock_update = mock_values.update.return_value
        
        df = pd.DataFrame({'A': [1], 'B': [2]})
        
        load_to_spreadsheet(df)
        
        mock_build.assert_called_with('sheets', 'v4', credentials=mock_credential)
        
        mock_values.update.assert_called()
        _, kwargs = mock_values.update.call_args
        self.assertEqual(kwargs['spreadsheetId'], 'TEST_ID')
        self.assertEqual(kwargs['range'], 'TEST_RANGE')
        self.assertEqual(kwargs['valueInputOption'], 'RAW')
        self.assertEqual(kwargs['body']['values'], [[1, 2]])

if __name__ == '__main__':
    unittest.main()
