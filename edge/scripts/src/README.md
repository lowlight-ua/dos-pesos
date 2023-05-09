To set up Greengrass on the edge device, copy these files to the Edge device and run the scripts there.

1. `greengrass`:
    * `setup.sh`: Installs Greengrass core software on the Edge device.
    * `uninstall.sh`: Uninstalls Greengrass core software.
2. `components`: After installing Greengrass core:
    * `setup.sh`: Initiates a Greengrass deployment to the Greengrass core device that will install the necessary Greengrass components.
    * `list.sh`: Lists the installed components, to verify the deployment.
