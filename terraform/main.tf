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
  name               = "c10-epsilon-lambda-test"
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
    function_name = "c10-epsilon-terraform-lambda-test"
    package_type = "Image"
    image_uri = data.aws_ecr_image.lambda-image.image_uri
}