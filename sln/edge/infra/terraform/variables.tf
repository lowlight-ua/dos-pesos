variable "region" {
  description = "The AWS region where resources will be created"
  type        = string
}

variable "core_iot_thing_name" {
    type        = string
}

variable "greengrass_group_name" {
    type        = string
}