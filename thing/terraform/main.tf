# https://docs.aws.amazon.com/greengrass/v2/developerguide/manual-installation.html


# -----------------------------------------------------------------------------


provider "aws" {
  region = var.region
}


# IoT Thing for client IoT device ---------------------------------------------

resource "aws_iot_thing" "client_iot_thing" {
  name = var.client_iot_thing_name
}


# GG group for the client IoT device ------------------------------------------

resource "aws_iot_thing_group" "gg_group" {
  name = var.greengrass_group_name
}

resource "aws_iot_thing_group_membership" "rel__gg_group__client_iot_thing" {
  thing_name = aws_iot_thing.client_iot_thing.name
  thing_group_name = aws_iot_thing_group.gg_group.name
}


# Credentials for the client IoT device ---------------------------------------

resource "aws_iot_certificate" "client_iot_thing__cert" {
  active = true
}

resource "local_file" "client_iot_thing__cert__certificate_pem_file" {
  content  = aws_iot_certificate.client_iot_thing__cert.certificate_pem
  filename = "client-iot-thing-certs/device.pem.crt"
}

resource "local_file" "client_iot_thing__cert__public_key_file" {
  content  = aws_iot_certificate.client_iot_thing__cert.public_key
  filename = "client-iot-thing-certs/public.pem.key"
}

resource "local_file" "client_iot_thing__cert__private_key_file" {
  content  = aws_iot_certificate.client_iot_thing__cert.private_key
  filename = "client-iot-thing-certs/private.pem.key"
}

resource "aws_iot_thing_principal_attachment" "rel__client_iot_thing__cert" {
  thing = aws_iot_thing.client_iot_thing.name
  principal = aws_iot_certificate.client_iot_thing__cert.arn
}


# AWS IoT policy for client IoT device ----------------------------------------

# AWS IoT policy that defines the AWS IoT permissions for the client IoT device. 
# The following policy allows access to all MQTT topics and Greengrass operations.

resource "aws_iot_policy_attachment" "rel__GreengrassV2IoTThingPolicy__cert" {
  policy = "GreengrassV2IoTThingPolicy"
  target = aws_iot_certificate.client_iot_thing__cert.arn
}


# Token exchange role ---------------------------------------------------------

# Create and attach an AWS IoT policy that allows the client IoT device 
# to use the role alias to assume the token exchange role. 

resource "aws_iot_policy_attachment" "rel_GreengrassV2IoTThingPolicy" {
  policy = "GreengrassCoreTokenExchangeRoleAliasPolicy"
  target = aws_iot_certificate.client_iot_thing__cert.arn
}


# associate-client-device-with-core-device ------------------------------------

resource "null_resource" "associate_client_device_with_core_device" {
  depends_on = [aws_iot_thing.client_iot_thing]

  triggers = {
    core_iot_thing_name = var.core_iot_thing_name
    client_iot_thing_name = var.client_iot_thing_name
  }

  provisioner "local-exec" {
    command = "aws greengrassv2 batch-associate-client-device-with-core-device --core-device-thing-name ${self.triggers.core_iot_thing_name} --entries thingName=${self.triggers.client_iot_thing_name}"
  }

  provisioner "local-exec" {
    when    = "destroy"
    command = "aws greengrassv2 batch-disassociate-client-device-with-core-device --core-device-thing-name ${self.triggers.core_iot_thing_name} --entries thingName=${self.triggers.client_iot_thing_name}"
  }
}
