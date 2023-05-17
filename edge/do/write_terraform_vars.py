import json
import os
from pathlib import Path

from do import util
from edge.do import ensure_config


def do() -> None:
    """
    Write out `terraform.tfvars.json` which provides values for Terraform variables
    that depend on the project configuration values.
    """

    master_cfg = ensure_config.config

    os.chdir(Path(__file__).parents[1])

    TERRAFORM_VARS = 'terraform/terraform.tfvars.json'

    print(f"Writing terraform variables to `{TERRAFORM_VARS}`.")
    tf_cfg = {
        'region': master_cfg["aws"]["region"],
        'core_iot_thing_name': master_cfg["greengrass_core"]["iot_thing_name"],
        'greengrass_group_name': master_cfg["greengrass_core"]["group_name"]
    }
    with open(TERRAFORM_VARS, "w") as tf_vars:
        tf_vars.write(json.dumps(tf_cfg, indent=4))


do()