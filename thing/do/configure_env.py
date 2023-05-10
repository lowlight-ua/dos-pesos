import os
import sys
import subprocess

sys.path.append(os.environ['DO_ROOT'])

from thing.do import \
    ensure_config, \
    run_terraform

print("Getting current edge connectivity info")

cmd = f"aws greengrassv2 get-connectivity-info --thing-name {ensure_config.config['greengrass_core']['iot_thing_name']} --output json"
connectivity_info = subprocess.check_output(thing_arn_command, shell=True).decode('utf-8')
print(f"    -> {connectivity_info}")

