import os
import shutil
import yaml
import json
import subprocess
from dotmap import DotMap

import util


paths = DotMap({
    'terraform_vars': 'terraform/terraform.tfvars.json',
    'src': 'scripts/src',
    'out': 'scripts/out',
    'greengrass_setup': {
        'download_dir': '/tmp/greengrass_setup'
    },
    'certs': 'terraform/greengrass-v2-certs'
}, _dynamic=False)


# ---------------------------------------------------------

def get_thing_arn():    
    thing_arn_command = f"aws iot describe-thing --thing-name {master_cfg['greengrass_core']['iot_thing_name']} --output json"
    print("    Getting thing ARN...")
    response = subprocess.check_output(thing_arn_command, shell=True).decode('utf-8')
    return json.loads(response)["thingArn"]


def get_iot_endpoints():
    print("    Getting IOT data endpoint...")
    data_endpoint_command = 'aws iot describe-endpoint --endpoint-type iot:Data-ATS --output text'
    data_endpoint = subprocess.check_output(data_endpoint_command, shell=True).strip().decode('utf-8')

    print("    Getting IOT credential provider endpoint...")
    cred_endpoint_command = 'aws iot describe-endpoint --endpoint-type iot:CredentialProvider --output text'
    cred_endpoint = subprocess.check_output(cred_endpoint_command, shell=True).strip().decode('utf-8')

    return data_endpoint, cred_endpoint


# ---------------------------------------------------------

if __name__ == "__main__":

    master_cfg = util.read_cfg('../config.yml') | util.read_cfg('config.yml')

    if util.contains_none(master_cfg):
        util.stop("No empty values are allowed in `config.yml`. Please fix and re-run the script.")

    print(f"Writing terraform variables to `{paths.terraform_vars}`.")
    tf_cfg = {
        'region': master_cfg["aws"]["region"],
        'iot_thing_name': master_cfg["greengrass_core"]["iot_thing_name"],
        'group_name': master_cfg["greengrass_core"]["group_name"]
    }
    with open(paths.terraform_vars, "w") as tf_vars:
        tf_vars.write(json.dumps(tf_cfg, indent=4))

    print("Gathering environment information...")
    try:
        thing_arn = get_thing_arn()
        iot_data, iot_cred = get_iot_endpoints()
    except subprocess.CalledProcessError:
        util.stop("Please run the terraform scripts and then re-run this script.")
    
    context = master_cfg | {
        'thingArn': thing_arn,
        'iotDataEndpoint': iot_data,
        'iotCredEndpoint': iot_cred,
        'paths': paths
    }

    try:
        shutil.copytree(paths.src, paths.out)
    except FileExistsError:
        util.stop(f"`{paths.out}` directory already exists. Remove it before proceeding.")

    shutil.copy(f"{paths.certs}/device.pem.crt", f"{paths.out}/greengrass")
    shutil.copy(f"{paths.certs}/private.pem.key", f"{paths.out}/greengrass")

    util.mkdir_if_missing(paths.greengrass_setup.download_dir)

    print("Generating setup scripts...")
    util.expand_jinja_templates(paths.out, context)