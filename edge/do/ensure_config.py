import os
import shutil
from pathlib import Path

from do import ensure_config, util

CONFIG = 'config.yml'
config = {}


def do():
    global config
    
    os.chdir(Path(__file__).parents[1])

    print("Ensuring edge config")

    if not os.path.isfile(CONFIG):
        shutil.copyfile(CONFIG + '.template', CONFIG)

    config = util.read_config(CONFIG)
    if util.contains_none(config):
        util.stop("Please fill out all values in " + os.path.abspath(CONFIG))

    config = ensure_config.config | config    


do()    
