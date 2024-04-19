provider "aws" {
    region = var.AWS_REGION
    access_key = var.AWS_ACCESS_KEY_ID
    secret_key = var.AWS_SECRET_ACCESS_KEY
}

data "aws_iam_policy_document" "lambda-role-policy" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "lambda-role" {
  name               = "c10-epsilon-lambda"
  assume_role_policy = data.aws_iam_policy_document.lambda-role-policy.json
}


data "aws_ecr_repository" "lambda-ecr-repo" {
  name = "c10-epsilon-plant-pipeline"
}

data "aws_ecr_image" "lambda-image" {
  repository_name = data.aws_ecr_repository.lambda-ecr-repo.name
  image_tag       = "latest"
}

resource "aws_lambda_function" "example-lambda" {
    role = aws_iam_role.lambda-role.arn
    function_name = "c10-epsilon-terraform-lambda-short-term"
    package_type = "Image"
    image_uri = data.aws_ecr_image.lambda-image.image_uri

    environment {
    variables = {
      DB_USER=var.DB_USER
      DB_PASSWORD=var.DB_PASSWORD
      DB_SCHEMA=var.DB_SCHEMA
      DB_HOST=var.DB_HOST
      DB_PORT=var.DB_PORT
      DB_NAME=var.DB_NAME
    }
  }

  timeout = 60 
}

