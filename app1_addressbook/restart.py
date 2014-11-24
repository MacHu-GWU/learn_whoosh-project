##encoding=utf8
import os
path = "indexdir"
for fname in os.listdir(path):
    os.remove(os.path.join(path, fname))