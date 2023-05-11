# Useless Greengrass project

## Overview

This project is an experiment in automation of the creation/provisionong of AWS Greengrass core devices and connected IoT things. You create and deploy any number of Greengrass cores, and any number of IoT things connected to the cores, by running CLI commands.

Automation takes care of:

* provisioning all the necessary AWS resources (stating from blank AWS account),
* installing and configuring Greengrass cores on edge devices, 
* configuring and connecting the Things, 
* and checking the resulting deployment by exchanging messages. 

The user only has to specify the AWS region and the desired names for these devices.

Deprovisioning/uninsallation is automatic as well.

Other than that, the project does nothing, so it's useless, though it's potentially useful as a project template.

## Why?

* Taste the life of a devops engineer. Try out Terraform.
* The complexity of AWS IoT projects felt challenging, and challenge accepted.
* Head start for a potential Greengrass project.
* Fun.

## Next steps?

* Introduce a useless custom Greengrass component (for message filtering/decoration)
* Introduce a useless back end, such as aS3 bucket for messages

## Further reading

* [Usage instructions](docs/usage.md)
* [Implementation description](docs/implementation.md)