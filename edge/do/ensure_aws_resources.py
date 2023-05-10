import json
import os
import subprocess
import sys

sys.path.append(os.environ['DO_ROOT'])

import shutil
from pathlib import Path

from do import util, ensure_aws_cli
from edge.do import ensure_config

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