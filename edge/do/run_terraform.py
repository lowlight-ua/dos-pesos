import os
import sys
import subprocess

sys.path.append(os.environ['DO_ROOT'])

from pathlib import Path

from edge.do import write_terraform_vars

os.chdir(Path(__file__).parents[1])

print("Running terraform to provision AWS resources required for the edge device")

os.chdir('terraform')
cmd = 'terraform apply'
print(f"Starting `{cmd}` in `{os.getcwd()}` ")

process = subprocess.Popen(cmd, shell=True)
process.communicate()

print(f"Finished `{cmd}` in `{os.getcwd()}` ")