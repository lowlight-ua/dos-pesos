# Creating account-level AWS resources

These steps will provision account-leve AWS resources required for the creation and operation of the edge devices. 

*These steps must only be done once per AWS account.*

**On any machine:**

* Install AWS CLI and log in as a sufficiently privileged principal. 

> You can attach the following policies to the principal:
>
> * `AWSIoTFullAccess`
> * `AmazonS3FullAccess`
> * `AWSGreengrassFullAccess`
> * `IAMFullAccess`

* `cd account/terraform`
* `terraform init`
* `terraform apply`

# Setting up an edge device

These steps will set up a new Greengrass core device by provisioning the necessary AWS resources and generating scripts to provision the edge on the desired machine. The edge device will be associated with the AWS account and resources mentioned above. Execute this steps for every Greengrass core you wish to create.

**On the development machine:**

* Install Python and Pip.
* Install Python dependencies: `pip3 install -r requirements.txt`
* Run the script `./do.sh edge/do/configure_env`
    * You will be guided through the necessary steps to set up dependencies, initialize configuration, and provision AWS resources necessary for the edge device.
    * Edge device provsioning scripts will be generated in `edge/scripts/out`.

**On the edge device:**

Set up the edge device by copying the files in `edge/scripts/out` from the development machine to the edge device and running the scripts over there. The edge device can be the development machine or a different machine. 

The provisioning scripts are:

1. `greengrass`:
    * `setup.sh`: Installs Greengrass core software on the Edge device.
    * `uninstall.sh`: Uninstalls Greengrass core software.
2. `components`: After installing Greengrass core:
    * `setup.sh`: Initiates a Greengrass deployment to the Greengrass core device that will install the necessary Greengrass components.
    * `check_deployment.sh`: Checks the status of the initiated deployment.
    * `list.sh`: Lists the installed components, to verify the deployment.


# Tearing down the edge device

**On the edge device:**

* Run the uninstall script (part of the `edge/scripts/out` bundle) on the edge machine.

**On the development machine:**

* `cd edge/terraform`
* `terraform destroy`

