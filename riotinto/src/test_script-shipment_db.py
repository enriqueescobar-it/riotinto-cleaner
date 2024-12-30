import unittest
import os
import duckdb
import pandas as pd
from pathlib import Path
from src.script_shipment_db import insert_row_, main


class TestScriptShipmentDB(unittest.TestCase):
    def setUp(self):
        """
        Set up a temporary environment for testing.
        """
        # Create a temporary directory for test files
        self.test_dir = Path("test_temp")
        self.test_dir.mkdir(exist_ok=True)
        
        # Create a sample CSV file with test data
        self.test_csv = self.test_dir / "test_data.csv"
        test_data = pd.DataFrame({
            'MovementDateTime': ['2019-07-20 00:00:00', '2023-01-01 12:34:56'],
            'Destination': ['Port1', 'Port2'],
            'DestinationTidied': ['Port1', 'Port2'],
            'Speed': [10.5, 15.0],
            'AdditionalInfo': ['Info1', 'Info2'],
            'CallSign': ['ABC123', 'DEF456'],
            'Heading': [90.0, 180.0],
            'MMSI': [123456789, 987654321],
            'MovementID': [1, 2],
            'ShipName': ['Ship1', 'Ship2'],
            'ShipType': ['Type1', 'Type2'],
            'Beam': [30.0, 40.0],
            'Draught': [5.0, 10.0],
            'Length': [200.0, 300.0],
            'ETA': ['2023-01-02 10:00:00', '2023-01-03 15:00:00'],
            'MoveStatus': ['Under way', 'Docked'],
            'LadenStatus': ['Laden', 'Ballast'],
            'LRIMOShipNo': [55555, 66666],
            'Latitude': [1.23, 4.56],
            'Longitude': [7.89, 10.11],
            'BeamRatio': [0.15, 0.13]
        })
        test_data.to_csv(self.test_csv, index=False)

        # Set up the output path for the DuckDB file
        self.output_dir = self.test_dir / "db"
        self.output_dir.mkdir(exist_ok=True)
        self.duckdb_file = self.output_dir / "shipment_db.duckdb"

    def tearDown(self):
        """
        Clean up temporary files after testing.
        """
        for file in self.test_dir.glob("**/*"):
            file.unlink()
        self.test_dir.rmdir()

    def test_insert_row(self):
        """
        Test the insert_row_ function directly.
        """
        conn = duckdb.connect(":memory:")  # In-memory DuckDB instance
        conn.execute('''
            CREATE TABLE shipments (
                MovementDateTime TIMESTAMP,
                Destination VARCHAR(255),
                DestinationTidied VARCHAR(255),
                Speed FLOAT,
                AdditionalInfo VARCHAR(255),
                CallSign VARCHAR(96),
                Heading FLOAT,
                MMSI BIGINT,
                MovementID BIGINT,
                ShipName VARCHAR(255),
                ShipType VARCHAR(96),
                Beam FLOAT,
                Draught FLOAT,
                Length FLOAT,
                ETA TIMESTAMP,
                MoveStatus VARCHAR(96),
                LadenStatus VARCHAR(96),
                LRIMOShipNo BIGINT,
                Latitude FLOAT,
                Longitude FLOAT,
                BeamRatio FLOAT
            );
        ''')
        test_row = {
            'MovementDateTime': '2019-07-20 00:00:00',
            'Destination': 'Port1',
            'DestinationTidied': 'Port1',
            'Speed': 10.5,
            'AdditionalInfo': 'Info1',
            'CallSign': 'ABC123',
            'Heading': 90.0,
            'MMSI': 123456789,
            'MovementID': 1,
            'ShipName': 'Ship1',
            'ShipType': 'Type1',
            'Beam': 30.0,
            'Draught': 5.0,
            'Length': 200.0,
            'ETA': '2023-01-02 10:00:00',
            'MoveStatus': 'Under way',
            'LadenStatus': 'Laden',
            'LRIMOShipNo': 55555,
            'Latitude': 1.23,
            'Longitude': 7.89,
            'BeamRatio': 0.15
        }
        insert_row_(conn, test_row)
        result = conn.execute("SELECT * FROM shipments").fetchdf()
        self.assertEqual(len(result), 1)
        self.assertEqual(result['Destination'].iloc[0], 'Port1')


if __name__ == '__main__':
    unittest.main()

