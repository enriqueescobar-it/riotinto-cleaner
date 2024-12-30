# Create the role
aws iam create-role --role-name RioTintoCleanerExecutionRole \
  --assume-role-policy-document file://riotinto-cleaner_role.json

# Attach the policy
aws iam put-role-policy --role-name RioTintoCleanerExecutionRole \
  --policy-name RioTintoCleanerPolicy \
  --policy-document file://riotinto-cleaner_policy.json
