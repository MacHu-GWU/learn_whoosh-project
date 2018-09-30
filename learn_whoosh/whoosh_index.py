# -*- coding: utf-8 -*-

import os
import shutil
from pathlib_mate import Path
from whoosh import index

from .config import Config


def get_index(schema, reset=True):
    if Path(Config.index_dir).exists():
        if reset:
            try:
                shutil.rmtree(Config.index_dir)
            except:
                pass
        else:
            idx = index.open_dir(Config.index_dir)
            return idx

    os.mkdir(Config.index_dir)
    idx = index.create_in(dirname=Config.index_dir, schema=schema)
    return idx
