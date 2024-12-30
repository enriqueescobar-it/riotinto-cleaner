#!/bin/bash

# Variables
AWS_USER="cliadminuser"
AWS_REGION="ca-central-1"
BUCKET_NAME="s3booker"
CONFIG_FILE="s3booker.json"

# Export AWS credentials (these should be replaced with secure methods for production use)
export AWS_ACCESS_KEY_ID="AKIAT"
export AWS_SECRET_ACCESS_KEY="eC1XJ"
export AWS_DEFAULT_REGION=$AWS_REGION

# Check if the bucket exists
BUCKET_EXISTS=$(aws s3api head-bucket --bucket $BUCKET_NAME 2>&1 || true)

if [[ -z $BUCKET_EXISTS ]]; then
  echo "Bucket $BUCKET_NAME already exists."
else
  echo "Bucket $BUCKET_NAME does not exist. Creating it now..."
  aws s3api create-bucket --bucket $BUCKET_NAME --region $AWS_REGION --create-bucket-configuration LocationConstraint=$AWS_REGION
  echo "Bucket $BUCKET_NAME created."
fi

# Apply event notifications from s3buck.json
if [[ -f $CONFIG_FILE ]]; then
  echo "Applying bucket notification configuration from $CONFIG_FILE..."
  aws s3api put-bucket-notification-configuration --bucket $BUCKET_NAME --notification-configuration file://$CONFIG_FILE
  echo "Notification configuration applied."
else
  echo "Configuration file $CONFIG_FILE not found. Skipping notification setup."
fi

# Check and create 'input_csv' folder if not exists
if aws s3api head-object --bucket $BUCKET_NAME --key input_csv/ 2>/dev/null; then
  echo "Folder 'input_csv' already exists in $BUCKET_NAME."
else
  echo "Creating 'input_csv' folder in $BUCKET_NAME..."
  aws s3api put-object --bucket $BUCKET_NAME --key input_csv/
  echo "'input_csv' folder created."
fi

# Check and create '_out' folder if not exists
if aws s3api head-object --bucket $BUCKET_NAME --key _out/ 2>/dev/null; then
  echo "Folder '_out' already exists in $BUCKET_NAME."
else
  echo "Creating '_out' folder in $BUCKET_NAME..."
  aws s3api put-object --bucket $BUCKET_NAME --key _out/
  echo "'_out' folder created."
fi

echo "Bucket $BUCKET_NAME and folder setup complete."

