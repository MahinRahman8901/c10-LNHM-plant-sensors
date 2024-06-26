
data "aws_iam_policy_document" "lambda-role-policy2" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }

  statement {
    sid       = "AmazonS3FullAccess"
    effect    = "Allow"
    actions   = ["s3:*"]
  }

  statement {
    actions   = ["s3-object-lambda:*"]
    effect    = "Allow"
    resources = ["*"]
  }

  statement {
    actions   = ["lambda:InvokeFunction"]
    effect    = "Allow"
    resources = ["*"]
  }
}

resource "aws_iam_role" "lambda-role2" {
  name               = "c10-epsilon-lambda-archive"
  assume_role_policy = data.aws_iam_policy_document.lambda-role-policy.json
}


data "aws_ecr_repository" "lambda-ecr-repo2" {
  name = "c10-epsilon-plant-archive"
}

data "aws_ecr_image" "lambda-image2" {
  repository_name = data.aws_ecr_repository.lambda-ecr-repo2.name
  image_tag       = "latest"
}

resource "aws_lambda_function" "example-lambda2" {
    role = aws_iam_role.lambda-role2.arn
    function_name = "c10-epsilon-terraform-lambda-archive"
    package_type = "Image"
    image_uri = data.aws_ecr_image.lambda-image2.image_uri

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

  timeout = 30 
}

