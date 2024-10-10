# Terraform

This folder contains Terraform files.

_It is Infrastructure-as-Code framework, responsible for project infrastructure provisioning._

# Contents:

- __tests__ - contains infrastructure unit tests

- __zipped_lambda_code__ - contains zipped lambda functions. These archives are uploaded to AWS. These are artifacts, no need to version control them. Source code is stored in `vehicles-monitoring/lambdas/` folder and version controlled.

- __terraform.tfvars.example__ - example of credentials required Terraform to access AWS. Rename to `terraform.tfvars` and input actual credentials to use.  