import os
import shutil
import sys
from pathlib import Path

sys.path.append(os.environ['DO_ROOT'])

from do import util

CONFIG = 'config.yml'

os.chdir(Path(__file__).parents[1])

print("Ensuring global config")

if not os.path.isfile(CONFIG):
    shutil.copyfile(CONFIG + '.template', CONFIG)

config = util.read_config(CONFIG)
if util.contains_none(config):
    util.stop("Please fill out all values in " + os.path.abspath(CONFIG))
