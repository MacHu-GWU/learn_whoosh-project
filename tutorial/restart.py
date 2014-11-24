##encoding=utf8

"""
a script to delete all files and folders in indexdir
"""

import os, shutil

def restart():
    path = "indexdir"
    for fname in os.listdir(path):
        try:
            os.remove(os.path.join(path, fname))
        except:
            shutil.rmtree(os.path.join(path, fname))
restart()