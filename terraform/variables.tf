variable "aws_access_key" {
  description = "AWS access key"
  type        = string
  sensitive   = true
}

variable "aws_secret_key" {
  description = "AWS secret key"
  type        = string
  sensitive   = true
}

variable "aws_region" {
  description = "The AWS region to deploy resources"
  type        = string
  default     = "eu-central-1"
}

variable "sqs_queue_name" {
  description = "Name of the SQS queue for vehicle tracking"
  type        = string
  default     = "vehicle-tracking"
}

variable "dynamodb_table_name" {
  description = "Name of the DynamoDB table for vehicle tracking"
  type        = string
  default     = "vehicle-tracking"
}

variable "lambda_role_name" {
  description = "The name of the IAM role for Lambda execution"
  type        = string
  default     = "lambda_executor_role"
}

variable "lambda_function_name" {
  description = "The name of the Lambda function"
  type        = string
  default     = "sqs-to-dynamodb"
}

variable "endpoint_address" {
  description = "AWS resources host"
  type        = string
  default     = "localhost"
}

variable "endpoint_port" {
  description = "Port used to acces AWS resourses at host"
  type        = string
  default     = "4566"
}