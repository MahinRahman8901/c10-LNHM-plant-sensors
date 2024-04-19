data "aws_iam_policy_document" "lambda_role_policy" {
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
  assume_role_policy = data.aws_iam_policy_document.lambda_role_policy.json

}

data "aws_ecr_repository" "lambda-ecr-repo3" {
  name = "c10-epsilon-plant-anomaly"
}


data "aws_ecr_image" "lambda-image3" {
  repository_name = data.aws_ecr_repository.lambda-ecr-repo3.name
  image_tag       = "latest"
}

resource "aws_lambda_function" "anomaly_lambda_function" {
  function_name = "c10-epsilon-plant-anomaly-lambda-tf"
  role = aws_iam_role.iam_for_lambda.arn
  package_type = "Image"
  image_uri = data.aws_ecr_image.lambda-image3.image_uri
  environment {
    variables = {
      DB_USER="epsilon"
      DB_PASSWORD="epsilon1"
      DB_SCHEMA="s_epsilon"
      DB_HOST="c10-plant-database.c57vkec7dkkx.eu-west-2.rds.amazonaws.com"
      DB_PORT="1433"
      DB_NAME="plants"
    }
  }
}




# Event Scheduling

data  "aws_iam_policy_document" "anomaly_schedule_trust_policy" {

    statement {
        effect = "Allow"

        principals {
            type        = "Service"
            identifiers = ["scheduler.amazonaws.com"]
        }

        actions = ["sts:AssumeRole"]
    }
}

# A permissions policy that allows things-attached-to-the-attached-role to do things
data  "aws_iam_policy_document" "anomaly_schedule_permissions_policy" {

    statement {
        effect = "Allow"

        resources = [
            aws_lambda_function.anomaly_lambda_function.arn
        ]

        actions = ["lambda:InvokeFunction"]
    }
}


# A role (which needs permissions & trust to actually do anything)
resource "aws_iam_role" "anomaly-schedule-role" {
    name               = "c10-epsilon-anomaly-schedule-role-tf"
    assume_role_policy = data.aws_iam_policy_document.anomaly_schedule_trust_policy.json # trust policy
    inline_policy {
      name = "c10-epsilon-inline-lambda-anomaly-execution-policy"
      policy = data.aws_iam_policy_document.anomaly_schedule_permissions_policy.json
    } # permissions policy
}



resource "aws_scheduler_schedule" "example" {
  name       = "my-schedule"
  group_name = "default"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression = "rate(1 hours)"

  target {
    arn      = aws_lambda_function.anomaly_lambda_function.arn
    role_arn = aws_iam_role.anomaly-schedule-role.arn
  }
}