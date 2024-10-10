provider "aws" {
  access_key                  = var.aws_access_key
  secret_key                  = var.aws_secret_key
  region                      = var.aws_region
  s3_use_path_style           = true
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    apigateway     = "http://${var.endpoint_address}:${var.endpoint_port}"
    cloudformation = "http://${var.endpoint_address}:${var.endpoint_port}"
    cloudwatch     = "http://${var.endpoint_address}:${var.endpoint_port}"
    dynamodb       = "http://${var.endpoint_address}:${var.endpoint_port}"
    ec2            = "http://${var.endpoint_address}:${var.endpoint_port}"
    es             = "http://${var.endpoint_address}:${var.endpoint_port}"
    elasticache    = "http://${var.endpoint_address}:${var.endpoint_port}"
    firehose       = "http://${var.endpoint_address}:${var.endpoint_port}"
    iam            = "http://${var.endpoint_address}:${var.endpoint_port}"
    kinesis        = "http://${var.endpoint_address}:${var.endpoint_port}"
    lambda         = "http://${var.endpoint_address}:${var.endpoint_port}"
    rds            = "http://${var.endpoint_address}:${var.endpoint_port}"
    redshift       = "http://${var.endpoint_address}:${var.endpoint_port}"
    route53        = "http://${var.endpoint_address}:${var.endpoint_port}"
    s3             = "http://s3.${var.endpoint_address}.localstack.cloud:${var.endpoint_port}"
    secretsmanager = "http://${var.endpoint_address}:${var.endpoint_port}"
    ses            = "http://${var.endpoint_address}:${var.endpoint_port}"
    sns            = "http://${var.endpoint_address}:${var.endpoint_port}"
    sqs            = "http://${var.endpoint_address}:${var.endpoint_port}"
    ssm            = "http://${var.endpoint_address}:${var.endpoint_port}"
    stepfunctions  = "http://${var.endpoint_address}:${var.endpoint_port}"
    sts            = "http://${var.endpoint_address}:${var.endpoint_port}"
  }
}


resource "aws_iam_role" "lambda_executor_role" {
  name = var.lambda_role_name

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

