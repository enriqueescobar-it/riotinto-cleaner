"""
    :module_name: function
    :module_summary: riotinto-cleaner description
    :module_author: Enrique Escobar
"""


import boto3
import pandas as pd
import numpy as np
from io import StringIO

# Initialize S3 client
s3_client = boto3.client('s3')


def datetime_normalize(data: pd.DataFrame, name: str) -> pd.DataFrame:
    data[name] = pd.to_datetime(data[name]).dt.strftime('%Y-%m-%dT%H:%M:%S')
    data[name] = data[name].astype(str)
    return data

def copy_and_convert_eta(data: pd.DataFrame, source_col: str, target_col: str) -> pd.DataFrame:
    data[target_col] = data[source_col].apply(
        lambda x: pd.NaT if x == "9999-12-31T23:59:59.000Z" else pd.to_datetime(x, errors='coerce')
    )
    return data

def clean_data_str(data: pd.DataFrame, name: str) -> pd.DataFrame:
    if name in data.columns:
        data[name] = data[name].astype(str)
        data[name] = data[name].replace('N/A', 'NA')
        data[name] = data[name].replace('nan', 'NA')
        data[name] = data[name].fillna('NA')
    return data

def clean_eta(data: pd.DataFrame) -> pd.DataFrame:
    d: pd.DataFrame = data.copy()
    d = d.drop(columns=['ETA'])
    d = d.rename(columns={'ETA2': 'ETA'})
    return d

# Fill missing or zero speeds for "Under way using engine"
def fill_missing_speeds(data: pd.DataFrame) -> pd.DataFrame:
    engine_data: pd.DataFrame = data[data['MoveStatus'] == 'Under way using engine']
    speed_means: pd.Series = engine_data[engine_data['Speed'] > 0].groupby('CallSign')['Speed'].mean()
    
    def fill_speed(row):
        if row['MoveStatus'] == 'Under way using engine' and (pd.isna(row['Speed']) or row['Speed'] == 0):
            return speed_means.get(row['CallSign'], row['Speed'])
        return row['Speed']
    
    data['Speed'] = data.apply(fill_speed, axis=1)
    return data

# Add the BeamRatio column
def calculate_beam_ratio(data: pd.DataFrame) -> pd.DataFrame:
    df: pd.DataFrame = data.copy()
    df['BeamRatio'] = np.where(
        df['Length'] == 0,
        np.nan,
        df['Beam'] / df['Length']
    )
    return df

def lambda_handler(event, context):
    """
    AWS Lambda function, process CSV files uploaded to 'input_csv/' folder.
    Enriched files are saved into the '_out/' folder with the same file name
    prefixed as 'pace-data_enriched'.
    """
    try:
        # Extract bucket and file key from the event
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        object_key = event['Records'][0]['s3']['object']['key']

        # Ensure we're processing only files in the 'input/' folder
        if not object_key.startswith("input/") or not object_key.endswith(".csv"):
            print(f"Ignoring file: {object_key}")
            return

        # Download the uploaded CSV file
        print(f"Processing file: {object_key} from bucket: {bucket_name}")
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        raw_data = response['Body'].read().decode('utf-8')

        # Load data into a Pandas DataFrame
        data: pd.DataFrame = pd.read_csv(StringIO(raw_data))
        data = data.rename(columns={'ladenStatus': 'LadenStatus'})
        # Perform data cleaning and enrichment
        print("Normalizing MovementDateTime...")
        data = datetime_normalize(data, 'MovementDateTime')

        print("Copying and converting ETA...")
        data = copy_and_convert_eta(data, 'ETA', 'ETA2')

        print("Cleaning string data...")
        data = clean_data_str(data, 'CallSign')

        print("Cleaning ETA column...")
        data = clean_eta(data)

        print("Filling missing speeds...")
        data = fill_missing_speeds(data)

        print("Calculating BeamRatio...")
        data = calculate_beam_ratio(data)

        # Save the enriched data to a new CSV in memory
        print("Saving enriched data to memory...")
        enriched_csv: StringIO = StringIO()
        data.to_csv(enriched_csv, index=False)
        enriched_csv.seek(0)

        # Create output key for enriched file
        output_key = object_key.replace("input_csv/", "_out/").replace(".csv", "_enriched.csv")

        # Upload the enriched file to S3
        print(f"Uploading enriched data to bucket: {bucket_name}, key: {output_key}")
        s3_client.put_object(Bucket=bucket_name, Key=output_key, Body=enriched_csv.getvalue())

        print("Data cleaning completed and saved to S3.")
        return {
            "statusCode": 200,
            "body": f"Data cleaned and saved to {output_key} in bucket {bucket_name}"
        }

    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return {
            "statusCode": 500,
            "body": f"Error processing file: {str(e)}"
        }
