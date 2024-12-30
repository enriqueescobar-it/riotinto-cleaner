import argparse
import pathlib
import sys
import os
import pandas as pd
import numpy as np


def load_data(input_file) -> pd.DataFrame:
    """Load the raw CSV file into a Pandas DataFrame."""
    return pd.read_csv(input_file)

# Normalize MovementDateTime to ISO format
def datetime_normalize(data: pd.DataFrame, name: str) -> pd.DataFrame:
    """Convert MovementDateTime to ISO format."""
    data[name] = pd.to_datetime(data[name]).dt.strftime('%Y-%m-%dT%H:%M:%S')
    data[name] = data[name].astype(str)
    return data

def copy_and_convert_eta(data: pd.DataFrame, source_col: str, target_col: str) -> pd.DataFrame:
    """
    Copy data from source_col to target_col, converting it to datetime.
    Replace '9999-12-31T23:59:59.000Z' with datetime.NaT in the target column.
    """
    data[target_col] = data[source_col].replace('9999-12-31T23:59:59.000Z', pd.NaT)
    data[target_col] = pd.to_datetime(data[target_col], errors='coerce')
    specified_date: pd.Timestamp = pd.Timestamp('2121-12-31 23:59:59')
    data[target_col] = data[target_col].fillna(specified_date)
    return data

def clean_data_str(data: pd.DataFrame, name: str) -> pd.DataFrame:
    """Clean the data by removing duplicates and handling missing values."""
    #data.drop_duplicates(inplace=True)
    #data.dropna(inplace=True)
    boo: bool = name in data.columns
    if boo:
        data[name] = data[name].astype(str)
        data[name] = data[name].replace('N/A', 'NA')
        data[name] = data[name].replace('nan', 'NA')
        data[name] = data[name].fillna('NA')
    return data

def clean_eta(data: pd.DataFrame) -> pd.DataFrame:
    d: pd.DataFrame = data.copy()
    # Drop the original 'ETA' column
    d = d.drop(columns=['ETA'])
    # Rename 'ETA2' to 'ETA'
    d = d.rename(columns={'ETA2': 'ETA'})
    return d

# Fill missing or zero speeds for "Under way using engine"
def fill_missing_speeds(data: pd.DataFrame) -> pd.DataFrame:
    """
    Fill missing or zero speeds for rows where MoveStatus is 'Under way using engine'.
    Missing speeds are replaced with the average speed for the respective CallSign.
    """
    # Filter rows with 'Under way using engine'
    engine_data = data[data['MoveStatus'] == 'Under way using engine']
    # Calculate mean speed per CallSign, excluding zeros and NaNs
    speed_means = engine_data[engine_data['Speed'] > 0].groupby('CallSign')['Speed'].mean()
    # Define a function to fill missing or zero speeds
    def fill_speed(row):
        if row['MoveStatus'] == 'Under way using engine' and (pd.isna(row['Speed']) or row['Speed'] == 0):
            return speed_means.get(row['CallSign'], row['Speed'])
        return row['Speed']
    # Apply the function to the Speed column
    data['Speed'] = data.apply(fill_speed, axis=1)
    return data

# Add the BeamRatio column
def calculate_beam_ratio(data):
    """
    Add a new feature BeamRatio as Beam / Length.
    """
    df: pd.DataFrame = data.copy()
    df['BeamRatio'] = np.where(
        df['Length'] == 0,
        np.nan,  # Return NaN when Length is 0
        df['Beam'] / df['Length']  # Normal calculation otherwise
    )
    return df

# Save the cleaned data to a new CSV file
def save_enriched_data(data: pd.DataFrame, output_file: str):
    """
    Save the cleaned and enriched data to a new CSV file.
    """
    data.to_csv(output_file, index=False)

def main():
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Text to DF.")
    parser.add_argument("-i", "--input-text", required=True, help="Text file")
    parser.add_argument('-o', '--output_path', required=True, help='Output path for resulting Text export')
    args: argparse.Namespace = parser.parse_args()
    input_text_str: str = args.input_text
    output_path: str = args.output_path
    text_basename: str = os.path.basename(input_text_str)
    text_name, text_extension = os.path.splitext(text_basename)
    print(input_text_str)
    print(text_basename)
    print(text_name, text_extension)
    print(output_path)
    full_file_path: str = os.path.join(output_path, f'{text_name}_enriched.csv')
    print(full_file_path)
    df: pd.DataFrame = load_data(input_text_str)
    df = datetime_normalize(df, 'MovementDateTime')
    df = clean_data_str(df, 'AdditionalInfo')
    df = clean_data_str(df, 'CallSign')
    df = clean_data_str(df, 'Destination')
    df = clean_data_str(df, 'DestinationTidied')
    df = clean_data_str(df, 'ShipName')
    df = clean_data_str(df, 'ShipType')
    df = clean_data_str(df, 'MoveStatus')
    df = clean_data_str(df, 'ladenStatus')
    df = df.rename(columns={'ladenStatus': 'LadenStatus'})
    df = copy_and_convert_eta(df, 'ETA', 'ETA2')
    df = datetime_normalize(df, 'ETA2')
    df = clean_eta(df)
    df = fill_missing_speeds(df)
    df = calculate_beam_ratio(df)
    print(df.columns, '\n', df.head(2).T, '\n', df.dtypes, '\n', df.BeamRatio.describe())
    save_enriched_data(df, full_file_path)

# python src/script.py -i data/raw/pace-data.csv -o data/processed/
if __name__ == "__main__":
    file_path: pathlib.PosixPath = pathlib.Path(sys.argv[4])
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 5 or (sys.argv[1] != '-i' and sys.argv[3] != '-o' and file_path.exists()):
        print("Usage: python script.py -i <input_text> -o <output_path>")
        sys.exit(1)
    else:
        main()
