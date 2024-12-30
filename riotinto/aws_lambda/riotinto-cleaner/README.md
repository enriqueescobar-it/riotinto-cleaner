# riotinto-cleaner

## About

riotinto-cleaner description

## Contributors

- Enrique Escobar

## Structure

Dockerfile: Defines a custom runtime for Lambda if needed (e.g., non-standard Python versions or libraries).
Makefile: Automates tasks like building, testing, and deploying.
README.md: Documents the project.
dev_requirements.txt: Dependencies for development (e.g., testing or linting tools like pytest, flake8).
requirements.txt: Production dependencies (e.g., libraries used by your Lambda function).
function.py: The Lambda function code.
test_function.py: Unit tests for the Lambda function.

## Test Local

### Virtual environment

python3 -m venv .venv
source .venv/bin/activate

### Dependencies

pip install -r dev_requirements.txt
pip install -r requirements.txt

### Run Tests

pytest test_function.py

### Lint code

flake8 function.py


### Template to run local SAM

```
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Resources:
  RiotintoCleanerFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: function.lambda_handler
      Runtime: python3.9
      CodeUri: .
      Timeout: 10
      MemorySize: 128
```

### Start a local API to invoke the Lambda

sam local start-api

### Test the endpoint

curl http://127.0.0.1:3000/

## Build package with SAM NOT WORKING

sam build

sam validate

sam local invoke

sam sync --stack-name riotinto-cleaner --watch

sam deploy --guided

sam package --s3-bucket 's3booker' --output-template-file riotinto-cleaner.yaml

sam deploy --template-file riotinto-cleaner.yaml --stack-name riotinto-cleaner --capabilities CAPABILITY_IAM

aws lambda invoke --function-name RiotintoCleanerFunction --payload '{}' response.json
cat response.json

## Check SAM security

aws iam list-attached-user-policies --user-name cliadminuser
aws iam list-attached-role-policies --role-name cliadminuser

aws iam attach-user-policy --policy-arn arn:aws:iam::aws:policy/AdministratorAccess --user-name cliadminuser

## AWS CLI only commands

### Setup pip3 Lambda Layer pandas309-layer

```bash
source osx309venv/bin/activate

LAYER_DIR="../pandas309-layer"
PACKAGE_DIR="$LAYER_DIR/python/lib/python3.9/site-packages"
LAYER_NAME="pandas309-layer"
LAYER_ZIP="$LAYER_NAME.zip"

# Create directories
mkdir -p $PACKAGE_DIR
pip3 install -r requirements.txt -t $PACKAGE_DIR

# Create the zip file
cd $LAYER_DIR
zip -r $LAYER_ZIP .

# Publish the layer to AWS Lambda
aws lambda publish-layer-version \
  --layer-name $LAYER_NAME \
  --description "Dependencies for RioTintoCleaner function Python 3.9" \
  --compatible-runtimes python3.9 \
  --zip-file fileb://$LAYER_ZIP

cd riotinto-cleaner
zip -r riotinto-cleaner.zip function.py

aws lambda create-function \
  --function-name RiotintoCleaner \
  --runtime python3.9 \
  --role arn:aws:iam::248864105438:role/RioTintoCleanerExecutionRole \
  --handler function.lambda_handler \
  --timeout 10 \
  --memory-size 128 \
  --zip-file fileb://riotinto-cleaner.zip

# Verify lambda ARN
aws lambda get-function --function-name RiotintoCleaner --region ca-central-1

# Lambda update
aws lambda update-function-code \
  --function-name RioTintoCleaner \
  --zip-file fileb://riotinto-cleaner.zip

# Add layers
aws lambda update-function-configuration \
  --function-name RiotintoCleaner \
  --layers arn:aws:lambda:ca-central-1:248864105438:layer:pandas309-layer:2 \
  --region ca-central-1

# Debugging optional
aws lambda update-function-configuration \
  --function-name RiotintoCleaner \
  --layers arn:aws:lambda:ca-central-1:248864105438:layer:pandas309-layer:2 \
  --region ca-central-1 --debug

# Verify Layer ARN
aws lambda get-function --function-name RiotintoCleaner --region ca-central-1

# Versions Layer
aws lambda list-layer-versions --layer-name pandas309-layer --region ca-central-1

```

### Setup pip3 packages

source osx309venv/bin/activate

mkdir package
pip3 install -r requirements.txt -t package/
#pip3 install --target ./package -r requirements.txt

### Setup ZIP file

cp function.py package/

cd package
zip -r ../riotinto-cleaner.zip .
cd ..

unzip -l riotinto-cleaner.zip

### Check if Lambda exists

aws lambda get-function --function-name RioTintoCleaner

### Deploy ZIP file with Execution Role

aws lambda create-function \
  --function-name RiotintoCleaner \
  --runtime python3.9 \
  --role arn:aws:iam::248864105438:role/RioTintoCleanerExecutionRole \
  --handler function.lambda_handler \
  --timeout 10 \
  --memory-size 128 \
  --zip-file fileb://riotinto-cleaner.zip

### Update ZIP file

aws lambda update-function-code \
  --function-name RiotintoCleaner \
  --zip-file fileb://riotinto-cleaner.zip

### Test Lambda

#### Lambda Test

riotinto-cleaner_test.json

```json
{
  "key1": "value1",
  "key2": "value2",
  "key3": "value3"
}
```

#### Lambda Run

aws lambda invoke --function-name RiotintoCleaner response.json

or

aws lambda invoke --function-name RioTintoCleaner \
  --payload fileb://riotinto-cleaner_test.json response.json

cat response.json

#### Logs View

aws logs describe-log-streams --log-group-name /aws/lambda/RiotintoCleaner

#### Logs Fetch

aws logs get-log-events --log-group-name /aws/lambda/RioTintoCleaner --log-stream-name <log-stream-name>


### Repeating LOOP

rm riotinto-cleaner.zip

zip -r riotinto-cleaner.zip package/ function.py

aws lambda update-function-code --function-name RiotintoCleaner \
  --memory-size 256 \
  --timeout 15 \
  --zip-file file://riotinto-cleaner.zip

#### Override function

aws lambda update-function-configuration \
  --function-name RioTintoCleaner \
  --environment Variables="{VAR1=value1,VAR2=value2}"

## Database

I use DuckDB because is better and less cumbersome than PostgreSQL or MySQL.

```bash
duckdb shipment_db.duckdb
ls -alhG

```
