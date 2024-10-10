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
