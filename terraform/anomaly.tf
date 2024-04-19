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

resource "aws_iam_role" "iam_for_lambda" {
  name               = "c10-epsilon-anomaly-terraform-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.lambda-role-policy.json
}

resource "aws_lambda_function" "anomaly_lambda_function" {

    function_name = "c10-epsilon-plant-anomaly-lambda-tf"
    role = aws_iam_role.iam_for_lambda.arn
    image_uri = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c10-epsilon-plant-anomaly:latest"
    environment {
    variables = {
    DB_USER="epsilon"
    DB_PASSWORD="epsilon1"
    DB_SCHEMA="s_epsilon"
    DB_HOST="c10-plant-database.c57vkec7dkkx.eu-west-2.rds.amazonaws.com"
    DB_PORT="1433"
    DB_NAME="plants"
    AWS_PUBLIC_KEY=variable.AWS_ACCESS_KEY_ID
    AWS_PRIVATE_KEY=variable.AWS_SECRET_ACCESS_KEY
    }
}
}

# Event Scheduling



resource "aws_scheduler_schedule" "example" {
  name       = "my-schedule"
  group_name = "default"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression = "rate(1 hours)"

  target {
    arn      = aws_sqs_queue.example.arn
    role_arn = aws_iam_role.example.arn
  }
}