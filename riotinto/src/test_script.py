import unittest
import pandas as pd
from src.script import (
    load_data,
    datetime_normalize,
    copy_and_convert_eta,
    clean_data_str,
    fill_missing_speeds,
    calculate_beam_ratio
)


class TestScriptFunctions(unittest.TestCase):

    def setUp(self):
        """
        Set up a test DataFrame to use across test cases.
        """
        self.test_data = pd.DataFrame({
            'MovementDateTime': ['2019-07-20 00:00:00', '2023-01-01 12:34:56'],
            'Speed': [0.0, 15.5],
            'CallSign': ['ABC123', 'DEF456'],
            'Beam': [30.0, 40.0],
            'Length': [200.0, 0.0],
            'ETA': ['9999-12-31T23:59:59.000Z', '2023-01-02T10:00:00'],
            'MoveStatus': ['Under way using engine', 'Moored']
        })

    def test_datetime_normalize(self):
        """Test the datetime_normalize function."""
        df = datetime_normalize(self.test_data.copy(), 'MovementDateTime')
        self.assertEqual(df['MovementDateTime'].iloc[0], '2019-07-20T00:00:00')
        self.assertEqual(df['MovementDateTime'].iloc[1], '2023-01-01T12:34:56')

    def test_copy_and_convert_eta(self):
        """Test the copy_and_convert_eta function."""
        df = copy_and_convert_eta(self.test_data.copy(), 'ETA', 'ETA2')
        self.assertNotIn('9999-12-31T23:59:59.000Z', df['ETA2'].astype(str).tolist())
        self.assertTrue(pd.Timestamp('2121-12-31 23:59:59') in df['ETA2'].tolist())

    def test_clean_data_str(self):
        """Test the clean_data_str function."""
        df = self.test_data.copy()
        df.loc[0, 'CallSign'] = 'nan'  # Simulate a NaN-like string
        df = clean_data_str(df, 'CallSign')
        self.assertEqual(df['CallSign'].iloc[0], 'NA')  # Replace 'nan' with 'NA'

    def test_calculate_beam_ratio(self):
        """Test the calculate_beam_ratio function."""
        df = calculate_beam_ratio(self.test_data.copy())
        self.assertAlmostEqual(df['BeamRatio'].iloc[0], 0.15, places=2)
        self.assertTrue(pd.isna(df['BeamRatio'].iloc[1]))  # Handle division by zero


if __name__ == '__main__':
    unittest.main()
