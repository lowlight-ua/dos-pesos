import os
import sys
import subprocess
import shutil
import json
from pathlib import Path

CERTS = 'terraform/client-iot-thing-certs'
OUT = 'out'
OUT_CERTS = 'out/certs'

sys.path.append(os.environ['DO_ROOT'])

from thing.do import \
    ensure_config, \
    run_terraform

print("Getting current edge connectivity info")

cmd = f"aws greengrassv2 get-connectivity-info --thing-name {ensure_config.config['greengrass_core']['iot_thing_name']} --output json"
connectivity_info = subprocess.check_output(cmd, shell=True).decode('utf-8')
print(f"    -> {connectivity_info}")

os.chdir(Path(__file__).parents[1])

print(f"Writing thing info to {os.path.abspath(OUT)}")

shutil.rmtree(OUT)
os.makedirs(OUT_CERTS)

shutil.copy(f"{CERTS}/device.pem.crt", OUT_CERTS)
shutil.copy(f"{CERTS}/private.pem.key", OUT_CERTS)

with open(f'{OUT}/mqtt.json', "w") as f:
    f.write(connectivity_info)
