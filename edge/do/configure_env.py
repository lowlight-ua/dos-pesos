import os
import sys
import shutil
from pathlib import Path

sys.path.append(os.environ['DO_ROOT'])

from do import util, ensure_aws_cli
from edge.do import \
    ensure_config, \
    run_terraform, \
    ensure_aws_resources \

print("Configuring development environment for edge")

paths = {
    'src': 'scripts/src',
    'out': 'scripts/out',

    'greengrass_setup': {
        'download_dir': '/tmp'
    },
    'certs': 'terraform/greengrass-v2-certs'
}

context = ensure_config.config | {
    'thingArn': ensure_aws_resources.thing_arn,
    'iotDataEndpoint': ensure_aws_resources.data_endpoint,
    'iotCredEndpoint': ensure_aws_resources.cred_endpoint,
    'paths': paths
}

os.chdir(Path(__file__).parents[1])

if os.path.isdir(paths["out"]):
    shutil.rmtree(paths["out"])
shutil.copytree(paths["src"], paths["out"])

shutil.copy(f"{paths['certs']}/device.pem.crt", f"{paths['out']}/greengrass")
shutil.copy(f"{paths['certs']}/private.pem.key", f"{paths['out']}/greengrass")

print(f"    Writing edge device setup scripts to `{paths['out']}`")
util.expand_jinja_templates(paths["out"], context)