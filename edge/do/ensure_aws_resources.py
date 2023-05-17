import json
import os
import subprocess
from pathlib import Path

from do import ensure_aws_cli, util
from edge.do import ensure_config


thing_arn = None
data_endpoint = None
cred_endpoint = None


def do():
    """
    Get info about the provisioned AWS resources for usage in some of the templates.
    """
    
    global thing_arn, data_endpoint, cred_endpoint

    os.chdir(Path(__file__).parents[1])

    master_cfg = ensure_config.config

    print("Ensuring AWS resources associated with the edge device")

    thing_arn_command = f"aws iot describe-thing --thing-name {master_cfg['greengrass_core']['iot_thing_name']} --output json"
    print("    Getting thing ARN...")
    response = subprocess.check_output(thing_arn_command, shell=True).decode('utf-8')
    thing_arn = json.loads(response)["thingArn"]
    print(f"    -> {thing_arn}")

    print("    Getting IOT data endpoint...")
    data_endpoint_command = 'aws iot describe-endpoint --endpoint-type iot:Data-ATS --output text'
    data_endpoint = subprocess.check_output(data_endpoint_command, shell=True).strip().decode('utf-8')
    print(f"    -> {data_endpoint}")

    print("    Getting IOT credential provider endpoint...")
    cred_endpoint_command = 'aws iot describe-endpoint --endpoint-type iot:CredentialProvider --output text'
    cred_endpoint = subprocess.check_output(cred_endpoint_command, shell=True).strip().decode('utf-8')
    print(f"    -> {cred_endpoint}")


do()