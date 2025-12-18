import unittest
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.transform import transform_to_DataFrame, transform_data, cleaned_data

class TestTransform(unittest.TestCase):

    def test_transform_to_DataFrame(self):
        data = [{"Title": " A ", "Price": " $10 ", "Rating": " 5 "}]
        df = transform_to_DataFrame(data)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 1)

    def test_transform_data_logic(self):
        # Raw data mimicking scrape result
        data = {
            "Title": [" Shirt ", " Pants ", "Unknown Product"],
            "Price": ["$10", "$20", "$0"],
            "Rating": ["Rating: 4.5", "Invalid Rating", "Not Rated"],
            "Colors": ["Colors 2", "1", "0"],
            "Size": ["Size: M", "L", "S"],
            "Gender": ["Gender: Men", "Women", "Unisex"],
            "Timestamp": ["2023-01-01", "2023-01-01", "2023-01-01"]
        }
        df = pd.DataFrame(data)
        exchange_rate = 15000

        # Execute
        transformed_df = transform_data(df, exchange_rate)

        self.assertEqual(len(transformed_df), 1)
        row = transformed_df.iloc[0]
        
        self.assertEqual(row["Title"], "Shirt")
        self.assertEqual(row["Price"], 10.0 * exchange_rate) # 150000.0
        self.assertEqual(row["Rating"], 4.5)
        self.assertEqual(row["Colors"], 2)
        self.assertEqual(row["Size"], "M")
        self.assertEqual(row["Gender"], "Men")

    def test_cleaned_data_duplicates_dropna(self):
        data = {
            "Title": ["A", "A", "B", "C"],
            "Price": [100, 100, 200, None]
        }
        df = pd.DataFrame(data)
        
        cleaned_df = cleaned_data(df)
        
        self.assertEqual(len(cleaned_df), 2)
        self.assertTrue("A" in cleaned_df["Title"].values)
        self.assertTrue("B" in cleaned_df["Title"].values)
        self.assertFalse("C" in cleaned_df["Title"].values)

if __name__ == '__main__':
    unittest.main()
