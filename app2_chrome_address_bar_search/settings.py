# -*- coding: utf-8 -*-

from pathlib_mate import Path
from learn_whoosh.browswer_bookmark.config import Config

Config.index_dir = Path(__file__).change(new_basename="index").abspath
