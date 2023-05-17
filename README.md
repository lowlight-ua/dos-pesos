# DosPesos – a useless Greengrass project

## Overview

*DosPesos* is an exercise in the automation of creation/provisioning of AWS Greengrass cores (edge devices) and the connected IoT things. You create and deploy any number of Greengrass cores, and any number of IoT things connected to the cores, by running CLI commands. Deprovisioning/uninstallation is automatic as well.

Automation takes care of:

* provisioning all the necessary AWS resources (stating from blank AWS account),
* installing and configuring Greengrass cores on edge devices, 
* configuring and connecting the Things, 
* and checking the resulting deployment by exchanging messages. 

The user only has to specify the AWS region and the desired names for these devices.

Other than that, the project does nothing, so it's useless, though it's potentially useful as a project template.

## Why?

* Get some devops skills. Try out Terraform.
* The complexity of AWS IoT projects felt challenging, challenge was accepted.
* Head start for a potential Greengrass project.
* Fun.

## Next steps?

* Introduce a useless custom Greengrass component (for message filtering/decoration)
* Introduce a useless back end, such as aS3 bucket for messages

## Further reading

* [Usage instructions](docs/usage.md)
* [Implementation notes](docs/implementation.md)