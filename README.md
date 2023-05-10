# Useless Greengrass project

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

* Wear a devops hat, try out Terraform.
* The complexity of AWS IoT projects feels challenging. It called me.

## Next steps?

* Introduce a useless custom Greengrass component (for message filtering/decoration)
* Introduce a useless back end, such as aS3 bucket for messages

# Creating account-level AWS resources

## Creating principal for automation

This step is not automated, because it requires a root access to the AWS account. The result of this step is a user on behalf of which the scripts will run.

*These steps must only be done once per AWS account.*

* Open the AWS IAM page in AWS console.
* Create a user and attach the following policies:
    * `AWSIoTFullAccess`
    * `AmazonS3FullAccess`
    * `AWSGreengrassFullAccess`
    * `IAMFullAccess`

## Global resources provisioning

These steps will provision account-leve AWS resources required for the creation and operation of the edge devices. 

*These steps must only be done once per AWS account.*

**On any machine:**

* Install AWS CLI and log in using the credentials of the user created above. 
* Run:
    * `cd account/terraform`
    * `terraform init`
    * `terraform apply`

# Edge device

## Setting up an edge device

These steps will set up a new Greengrass core device by provisioning the necessary AWS resources and generating scripts to provision the edge on the desired machine. The edge device will be associated with the AWS account and resources mentioned above. 

*You can run these steps as many times as you want, for every Greengrass core you wish to create.*

**(1) On the development machine:**

* Install Python and Pip.
* Install Python dependencies: `pip3 install -r requirements.txt`
* Run the script `./do.sh edge/do/configure_env`
    * You will be guided through the necessary steps to set up dependencies, initialize configuration, and provision AWS resources necessary for the edge device.
    * Edge device provsioning scripts will be generated in `edge/scripts/out`.

**(2) On the edge device:**

Set up the edge device by copying the files in `edge/scripts/out` from the development machine to the edge device and running the scripts over there. The edge device can be the development machine or a different machine. 

The provisioning scripts are:

1. `greengrass`:
    * `setup.sh`: Automatically installs and configures Greengrass core software on the Edge device.
    * `uninstall.sh`: Uninstalls Greengrass core software.
2. `components`: After installing Greengrass core:
    * `setup.sh`: Initiates a Greengrass deployment to the Greengrass core device that will install the necessary Greengrass components, such as the MQTT broker.
    * `check_deployment.sh`: Checks the status of the initiated deployment. After running `setup.sh` you may run this periodically until the deployment has completed.
    * `list.sh`: Lists the installed components, to verify the deployment.

## Tearing down the edge device

**On the edge device:**

* Run the uninstall script (part of the `edge/scripts/out` bundle) on the edge machine.

**On the development machine:**

* `cd edge/terraform`
* `terraform destroy`

# IoT thing

## Creating an IoT thing

These steps will set up a new IoT thing by provisioning the necessary AWS resources, associating the IoT thing with the Greengrass core, and generating files to provision the IoT thing on the desired machine. The IoT thing will then be ready to connect to the Edge device created in the previous step. 

*You may execute these steps many times for every IoT thing you wish to create.*

**On the development machine:**

* Run the script `./do.sh thing/do/configure_env`
    * You will be guided through the necessary steps to set up dependencies, initialize configuration, and provision AWS resources necessary for the edge device.
    * Files required to provision the IoT thing will be generated in `thing/out`.

**On the IoT thing machine:**

This section describes how to create a temporary Thing for testing purposes.

* Install Python and Pip.
* Install the AWS IoT Device SDK v2 for Python:
    * `git clone https://github.com/aws/aws-iot-device-sdk-python-v2.git`
    * In the cloned repo: `python3 -m pip install --user ./aws-iot-device-sdk-python-v2`
* Navigate to `aws-iot-device-sdk-python-v2/samples`
* From `thing/out` on the development machine, copy the files here.
* **Option 1** (uses cloud discovery): Run `basic_discovery.sh`. You should see messages indicating that the IoT thing connected to Greengrass core and sent a few messages.
* **Option 2**: (does not use cloud discovery) (Todo automate) Run the following. Replace "???" with the info from `mqtt.json`, and copy `ca.pem` from `<greengrass_core_rootpath>/work/aws.greengrass.clientdevices.Auth/ca.pem` on the edge device machine.

```
python3 pubsub.py --endpoint ??? --port ??? --cert device.pem.crt --key private.pem.key --ca_file ca.pem --client_id ???
```

## Deprovisioning an IoT thing

**On the development machine:**

* `cd thing/terraform`

* ##### `terraform destroy`

