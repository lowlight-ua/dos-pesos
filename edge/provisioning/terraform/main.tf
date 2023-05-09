# https://docs.aws.amazon.com/greengrass/v2/developerguide/manual-installation.html


# -----------------------------------------------------------------------------


provider "aws" {
  region = var.region
}


# IoT Thing for Greengrass core device ----------------------------------------

resource "aws_iot_thing" "core_iot_thing" {
  name = var.core_iot_thing_name
}


# GG group for the Greengrass core device -------------------------------------

resource "aws_iot_thing_group" "gg_group" {
  name = var.greengrass_group_name
}

resource "aws_iot_thing_group_membership" "rel__gg_group__core_iot_thing" {
  thing_name = aws_iot_thing.core_iot_thing.name
  thing_group_name = aws_iot_thing_group.gg_group.name
}


# Credentials for the Greengrass core device ----------------------------------

resource "aws_iot_certificate" "core_iot_thing__cert" {
  active = true
}

resource "local_file" "core_iot_thing__cert__certificate_pem_file" {
  content  = aws_iot_certificate.core_iot_thing__cert.certificate_pem
  filename = "greengrass-v2-certs/device.pem.crt"
}

resource "local_file" "core_iot_thing__cert__public_key_file" {
  content  = aws_iot_certificate.core_iot_thing__cert.public_key
  filename = "greengrass-v2-certs/public.pem.key"
}

resource "local_file" "core_iot_thing__cert__private_key_file" {
  content  = aws_iot_certificate.core_iot_thing__cert.private_key
  filename = "greengrass-v2-certs/private.pem.key"
}

resource "aws_iot_thing_principal_attachment" "rel__core_iot_thing__cert" {
  thing = aws_iot_thing.core_iot_thing.name
  principal = aws_iot_certificate.core_iot_thing__cert.arn
}


# AWS IoT policy for Greengrass core device -----------------------------------

# AWS IoT policy that defines the AWS IoT permissions for the Greengrass core device. 
# The following policy allows access to all MQTT topics and Greengrass operations.

resource "aws_iot_policy_attachment" "rel__GreengrassV2IoTThingPolicy__cert" {
  policy = "GreengrassV2IoTThingPolicy"
  target = aws_iot_certificate.core_iot_thing__cert.arn
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

# Here: Create a token exchange IAM role and an AWS IoT role alias that points 
# to the role. 

# 1. Create an IAM role that device can use as a token exchange role.  

# 3. Create and attach an AWS IoT policy that allows the Greengrass core device 
# to use the role alias to assume the token exchange role. 

resource "aws_iot_policy_attachment" "rel_GreengrassV2IoTThingPolicy" {
  policy = "GreengrassCoreTokenExchangeRoleAliasPolicy"
  target = aws_iot_certificate.core_iot_thing__cert.arn
}
