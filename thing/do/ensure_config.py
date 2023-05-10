import os
import sys

sys.path.append(os.environ['DO_ROOT'])

import shutil
from pathlib import Path

from do import util, ensure_config

CONFIG = 'config.yml'

os.chdir(Path(__file__).parents[1])

print("Ensuring thing config")

if not os.path.isfile(CONFIG):
    shutil.copyfile(CONFIG + '.template', CONFIG)

config = util.read_config(CONFIG)
if util.contains_none(config):
    util.stop("Please fill out all values in " + os.path.abspath(CONFIG))

config = ensure_config.config | config