import os
import sys

sys.path.append(os.environ['DO_ROOT'])

from do import util

print("Checking AWS CLI")

util.check_program_availability('aws')
if not util.check_successful_execution('aws sts get-caller-identity'):
    util.stop("AWS CLI not logged in.")