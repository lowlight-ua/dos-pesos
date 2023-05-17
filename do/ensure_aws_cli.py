import os
import sys

from do import util


def do() -> None:
    """
    Ensures AWS CLI is installed and configured with credentials.
    """

    print("Checking AWS CLI")

    util.check_program_availability('aws')
    if not util.check_successful_execution('aws sts get-caller-identity'):
        util.stop("AWS CLI not logged in.")

do()