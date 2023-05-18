import os
import shutil
import subprocess
from pathlib import Path

import requests

CERTS = 'terraform/client-iot-thing-certs'
OUT = 'out'

from sln.thing.do import ensure_config, run_terraform


def do() -> None:
    """
    Configures the working copy of the project for the client IoT thing as
    specified in the configuration files. Generates file that can be used
    to provision a client IoT thing.
    """

    print("Getting current edge connectivity info")

    cmd = f"aws greengrassv2 get-connectivity-info --thing-name {ensure_config.config['greengrass_core']['iot_thing_name']} --output json"
    connectivity_info = subprocess.check_output(cmd, shell=True).decode('utf-8')
    print(f"    -> {connectivity_info}")

    os.chdir(Path(__file__).parents[1])

    print(f"Writing thing info to {os.path.abspath(OUT)}")

    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)

    shutil.copy(f"{CERTS}/device.pem.crt", OUT)
    shutil.copy(f"{CERTS}/private.pem.key", OUT)

    with open(f'{OUT}/AmazonRootCA1.pem', "wb") as f:
        pem = requests.get('https://www.amazontrust.com/repository/AmazonRootCA1.pem')
        f.write(pem.content)

    with open(f'{OUT}/mqtt.json', "w") as f:
        f.write(connectivity_info)

    iot_thing_name = ensure_config.config['client_iot_thing']['iot_thing_name']
    region = ensure_config.config["aws"]["region"]

    with open(f'{OUT}/thing_info.json', "w") as f:
        cmd = f"aws iot describe-thing --thing-name {iot_thing_name} --output json"
        f.write(subprocess.check_output(cmd, shell=True).decode('utf-8'))

    with open(f'{OUT}/basic_discovery.sh', "w") as f:
        s = f"""python3 basic_discovery.py \\
            --thing_name {iot_thing_name} \\
            --topic 'clients/{iot_thing_name}/hello/world' \\
            --message 'Hello World!' \\
            --ca_file AmazonRootCA1.pem \\
            --cert device.pem.crt \\
            --key private.pem.key \\
            --region {region} \\"""
        f.write(s)

    os.chmod(f'{OUT}/basic_discovery.sh', 0o755)


do()    