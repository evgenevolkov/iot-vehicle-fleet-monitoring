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

resource "aws_sqs_queue" "vehicle_tracking" {
  name                              = var.sqs_queue_name
  fifo_queue                        = false
  message_retention_seconds         = 3600
}

resource "aws_dynamodb_table" "vehicle_tracking" {
  name         = var.dynamodb_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "vehicle_id"

  attribute {
    name = "vehicle_id"
    type = "S"
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

resource "aws_iam_policy" "lambda_executor_policy" {
  name = "lambda_executor_policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes"
        ],
        Resource = aws_sqs_queue.vehicle_tracking.arn
      },
      {
        Effect = "Allow",
        Action = [
          "dynamodb:PutItem"
        ],
        Resource = aws_dynamodb_table.vehicle_tracking.arn
      },
      {
        Effect = "Allow",
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_executor_attachment" {
  role       = aws_iam_role.lambda_executor_role.name
  policy_arn = aws_iam_policy.lambda_executor_policy.arn
}

resource "aws_lambda_function" "sqs_to_dynamodb" {
  function_name = var.lambda_function_name
  role          = aws_iam_role.lambda_executor_role.arn
  runtime       = "python3.9"
  handler       = "lambda_function.lambda_handler"
  filename      = "zipped_lambda_code/sqs_to_dynamodb/lambda.zip"

  environment {
    variables = {
      DYNAMODB_TABLE = aws_dynamodb_table.vehicle_tracking.name
    }
  }
}