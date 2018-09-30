# -*- coding: utf-8 -*-

import os
import shutil
from pathlib_mate import Path
from whoosh import index

from .config import Config
from .whoosh_schema import bookmark_schema


def get_index(reset=True):
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
    idx = index.create_in(dirname=Config.index_dir, schema=bookmark_schema)
    return idx
