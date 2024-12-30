aws iam list-attached-user-policies --user-name cliadminuser
aws iam list-attached-role-policies --role-name cliadminuser

aws iam attach-user-policy --policy-arn arn:aws:iam::aws:policy/AdministratorAccess --user-name cliadminuser


aws iam attach-user-policy --user-name cliadminuser \
  --policy-arn arn:aws:iam::aws:policy/AWSLambda_FullAccess

aws iam attach-user-policy --user-name cliadminuser \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

aws iam attach-user-policy --user-name cliadminuser \
  --policy-arn arn:aws:iam::aws:policy/CloudWatchLogsFullAccess

