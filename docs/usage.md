# Creating instance-level AWS resources

## Creating user for automation

This step is not automated, because it requires a root access to the AWS account. The result of this step is a user on behalf of which the scripts will run.

*These steps must only be done once per instance.*

* Open the AWS IAM page in AWS console.
* Create a user and attach the following policies:
    * `AWSIoTFullAccess`
    * `AmazonS3FullAccess`
    * `AWSGreengrassFullAccess`
    * `IAMFullAccess`

## Global resources provisioning

These steps will provision instance-level AWS resources required for the creation and operation of the edge devices. 

*These steps must only be done once per AWS instance.*

**On any machine:**

* Install Python and Pip.
* Install Python dependencies: `pip3 install -r requirements.txt`
* Run the script `./do.sh sln/instance/do/init_instance`
    * You will be guided through the necessary steps to set up dependencies and provision AWS resources necessary for the instance.

# Edge device

## Setting up an edge device

These steps will set up a new Greengrass core device by provisioning the necessary AWS resources and generating scripts to provision the edge on the desired machine. The edge device will be associated with the AWS account and resources mentioned above. 

*You can run these steps as many times as you want, for every Greengrass core you wish to create.*

**(1) On the development machine:**

* Install Python and Pip.
* Install Python dependencies: `pip3 install -r requirements.txt`
* Run the script `./do.sh sln/edge/infra/do/configure_project`
    * You will be guided through the necessary steps to set up dependencies, initialize configuration, set up the working copy of the project, and provision AWS resources necessary for the edge device.
    * Edge device provisioning scripts will be generated in `sln/edge/infra/scripts/out`.

**(2) On the edge device:**

Instal the Greengrass core: copy the files in `sln/edge/infra/scripts/out/core` from the development machine to the edge device and run the script over there. (If the edge device machine is the same as the developer machine, you can run the script in place.)

**(3) On the development machine:**

Install the required AWS-provided Greengrass components by running `sln/edge/infra/scripts/components/deploy.sh`. Also in this directory:

* `check_deployment.sh`: Checks the status of the initiated component deployment. After running `setup.sh` you may run this periodically until the deployment has completed.
* `list.sh`: Lists the installed components, to verify the deployment.

## Tearing down the edge device

**On the edge device:**

* Run the uninstall script (part of the `sln/edge/infra/scripts/out` bundle) on the edge machine.

**On the development machine:**

* `cd sln/edge/infra/terraform`
* `terraform destroy`

# IoT thing

## Creating an IoT thing

These steps will set up a new IoT thing by provisioning the necessary AWS resources, and associating the IoT thing with the Greengrass core. 

It will also generate files that will help you set up a temporary software-defined IoT thing in order to test the connection to the Greengrass core (this IoT thing will then be ready to connect to the Edge device created in the previous step). Using the credentials and connection information, you will later be able to configure an actual IoT Thing.

*You may execute these steps many times for every IoT thing you wish to create.*

**On the development machine:**

* Run the script `./do.sh sln/thing/do/configure_project`
    * You will be guided through the necessary steps to set up dependencies, initialize configuration, set up the working copy of the project, and provision AWS resources necessary for the edge device.
    * Files required to provision the IoT thing will be generated in `sln/thing/out`.

**On the IoT thing machine:**

This section describes how to create a temporary Thing to test the connection to the Greengrass core.

* Install Python and Pip.
* Install the AWS IoT Device SDK v2 for Python:
    * `git clone https://github.com/aws/aws-iot-device-sdk-python-v2.git`
    * `python3 -m pip install --user ./aws-iot-device-sdk-python-v2`
* Navigate to `aws-iot-device-sdk-python-v2/samples`
* From `sln/thing/out` on the development machine, copy the files here.
* **Option 1** (uses cloud discovery): Run `basic_discovery.sh`. You should see messages indicating that the IoT thing connected to Greengrass core and sent a few messages.
* **Option 2**: (does not use cloud discovery) (Todo automate) Run the following. Replace "???" with the info from `mqtt.json`, and copy `ca.pem` from `<greengrass_core_rootpath>/work/aws.greengrass.clientdevices.Auth/ca.pem` on the edge device machine. The `client_id` is the name of your client thing from the config you provided.

```
python3 pubsub.py --endpoint ??? --port ??? --cert device.pem.crt --key private.pem.key --ca_file ca.pem --client_id ???
```

## Deprovisioning an IoT thing

**On the development machine:**

* `cd sln/thing/terraform`
* `terraform destroy`

# Checking what Things you have provisioned

Active Things (edge devices and client things) can incur charges to your AWS account. Use `list_things.sh` to show what edges and client things you have provisioned in an instance.