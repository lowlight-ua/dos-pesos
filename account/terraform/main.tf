# AWS IoT policy for Greengrass core device -----------------------------------

# AWS IoT policy that defines the AWS IoT permissions for the Greengrass core device. 
# The following policy allows access to all MQTT topics and Greengrass operations.

resource "aws_iot_policy" "aws_iot__core_iot_thing" {
  name = "GreengrassV2IoTThingPolicy"

  policy = jsonencode(
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": [
            "iot:Publish",
            "iot:Subscribe",
            "iot:Receive",
            "iot:Connect",
            "greengrass:*",
            "iot:GetThingShadow",
            "iot:UpdateThingShadow",
            "iot:DeleteThingShadow"
          ],
          "Resource": [
            "*"
          ]
        }
      ]
    }    
  )
}


# Token exchange role ---------------------------------------------------------

# Greengrass core devices use an IAM service role, called the token exchange role, 
# to authorize calls to AWS services. The device uses the AWS IoT credentials provider 
# to get temporary AWS credentials for this role, which allows the device to interact 
# with AWS IoT, send logs to Amazon CloudWatch Logs, and download custom component 
# artifacts from Amazon S3. 

# You use an AWS IoT role alias to configure the token exchange role for Greengrass 
# core devices. Role aliases enable you to change the token exchange role for a device 
# but keep the device configuration the same. 

resource "aws_iam_role" "greengrass_v2_token_exchange" {
  name               = "GreengrassV2TokenExchangeRole"
  assume_role_policy = jsonencode(
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": {
            "Service": "credentials.iot.amazonaws.com"
          },
          "Action": "sts:AssumeRole"
        }
      ]
    }
  )
}

resource "aws_iot_role_alias" "greengrass_v2_token_exchange_alias" {
  alias = "GreengrassCoreTokenExchangeRoleAlias"
  role_arn = aws_iam_role.greengrass_v2_token_exchange.arn
}

resource "aws_iam_policy" "greengrass_v2_token_exchange_role_access" {
  name        = "GreengrassV2TokenExchangeRoleAccess"
  policy      = jsonencode(
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": [
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:PutLogEvents",
            "logs:DescribeLogStreams",
            "s3:GetBucketLocation"
          ],
          "Resource": "*"
        }
      ]
    }
  )
}

resource "aws_iam_role_policy_attachment" "rel_policy_greengrass_v2_token_exchange" {
  policy_arn = aws_iam_policy.greengrass_v2_token_exchange_role_access.arn
  role       = aws_iam_role.greengrass_v2_token_exchange.name
}

resource "aws_iot_policy" "GreengrassCoreTokenExchangeRoleAliasPolicy" {
  name = "GreengrassCoreTokenExchangeRoleAliasPolicy"

  policy = jsonencode(
    {
      "Version":"2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": "iot:AssumeRoleWithCertificate",
          "Resource": "${aws_iot_role_alias.greengrass_v2_token_exchange_alias.arn}"
        }
      ]
    }
  )
}


# Greengrass service role -----------------------------------------------------

resource "aws_iam_role" "greengrass_service_role" {
  name = "Greengrass_ServiceRole"

  assume_role_policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Service": "greengrass.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "rel__greengrass_service_role" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGreengrassResourceAccessRolePolicy"
  role = aws_iam_role.greengrass_service_role.name
}

resource "null_resource" "associate_greengrassv2_service_role" {
  depends_on = [aws_iam_role.greengrass_service_role]

  provisioner "local-exec" {
    command = "aws greengrassv2 associate-service-role-to-account --role-arn ${aws_iam_role.greengrass_service_role.arn}"
  }

  provisioner "local-exec" {
    when    = "destroy"
    command = "aws greengrassv2 disassociate-service-role-from-account"
  }

  triggers = {
    role_arn = aws_iam_role.greengrass_service_role.arn
  }
}

