import os
import subprocess
from pathlib import Path

from do import util
from edge.do import write_terraform_vars


def do() -> None:
    """Execute the Terraform scripts to provision AWS resources required for
    a Greengrass core device."""

    os.chdir(Path(__file__).parents[1])

    print("Running terraform to provision AWS resources required for the edge device")
    util.check_program_availability('terraform')

    os.chdir('terraform')
    cmd = 'terraform init && terraform apply'
    print(f"Starting `{cmd}` in `{os.getcwd()}` ")

    process = subprocess.Popen(cmd, shell=True)
    process.communicate()

    print(f"Finished `{cmd}` in `{os.getcwd()}` ")


do()    