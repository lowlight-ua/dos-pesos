output "core_iot_thing__cert__certificate_pem" {
    value = aws_iot_certificate.core_iot_thing__cert.certificate_pem
    sensitive = true
}

output "core_iot_thing__cert__public_key" {
    value = aws_iot_certificate.core_iot_thing__cert.public_key
    sensitive = true
}

output "core_iot_thing__cert__private_key" {
    value = aws_iot_certificate.core_iot_thing__cert.private_key
    sensitive = true
}