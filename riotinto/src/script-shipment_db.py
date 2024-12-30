import argparse
import pathlib
import sys
import os
import duckdb
import pandas as pd


def insert_row_(conn, row):
    try:
        conn.execute("""
            INSERT INTO shipments (
                MovementDateTime, Destination, DestinationTidied, Speed, AdditionalInfo,
                CallSign, Heading, MMSI, MovementID, ShipName,
                ShipType, Beam, Draught, Length, ETA,
                MoveStatus, LadenStatus, LRIMOShipNo, Latitude, Longitude,
                BeamRatio
            ) VALUES (?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?,
            ?)
        """, (
            row['MovementDateTime'], row['Destination'], row['DestinationTidied'], row['Speed'], row['AdditionalInfo']
            , row['CallSign'], row['Heading'], row['MMSI'], row['MovementID'], row['ShipName']
            , row['ShipName'], row['Beam'], row['Draught'], row['Length'], row['ETA']
            , row['MoveStatus'], row['LadenStatus'], row['LRIMOShipNo'], row['Latitude'], row['Longitude']
            , row['BeamRatio']
        ))
    except Exception as e:
        print(f"Error inserting row {row.name}: {e}")

def main():
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Text to DF.")
    parser.add_argument("-i", "--input-text", required=True, help="Text file")
    parser.add_argument('-o', '--output_path', required=True, help='Output path for DB export')
    args: argparse.Namespace = parser.parse_args()
    input_text_str: str = args.input_text
    output_path: str = args.output_path
    text_basename: str = os.path.basename(input_text_str)
    text_name, text_extension = os.path.splitext(text_basename)
    print(input_text_str)
    print(text_basename)
    print(text_name, text_extension)
    print(output_path)
    full_file_path: str = os.path.join(output_path, 'shipment_db.duckdb')
    print(full_file_path)
    df: pd.DataFrame = pd.read_csv(input_text_str)
    # Connect to (or create) the DuckDB database
    conn = duckdb.connect(full_file_path)
    # Optional: Create a table in the database
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
        BeamRatio FLOAT);
    ''')
    print("Database and table created successfully.")
    # Iterate through the DataFrame and insert rows one by one
    print(df.columns)
    for index, row in df.iterrows():
        #print(index, row['MovementDateTime'], row['ETA'], row['BeamRatio'])
        insert_row_(conn, row)
    # List the first 2 rows from the shipments table
    first_five_rows = conn.execute("SELECT * FROM shipments LIMIT 2").fetchdf()
    # Count the total number of rows in the shipments table
    total_rows = conn.execute("SELECT COUNT(*) FROM shipments").fetchone()[0]
    # Print the results
    print("First 2 rows of the shipments table:")
    print(first_five_rows)
    print("\nTotal number of rows in the shipments table:")
    print(total_rows)

# python src/script-shipment_db.py -i data/processed/pace-data_enriched.csv -o db/duckdb/
if __name__ == "__main__":
    file_path: pathlib.PosixPath = pathlib.Path(sys.argv[4])
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 5 or (sys.argv[1] != '-i' and sys.argv[3] != '-o' and file_path.exists()):
        print("Usage: python script.py -i <input_text> -o <output_path>")
        sys.exit(1)
    else:
        main()