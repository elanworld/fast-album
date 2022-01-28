# 创建可复制直接运行的虚拟环境
import os
import shutil
from common import python_box

import sys

if __name__ == '__main__':
    python_dir = os.path.dirname(sys.executable)
    dst = "venv"
    dir_list = python_box.dir_list(python_dir, walk=True)
    filter_str = os.path.join(r"Lib\site-packages")
    if not os.path.exists(dst):
        os.system(f"python -m venv {dst}")
        os.system(f"pip install -r requirements.txt")
    for path in dir_list:
        if filter_str in path:
            continue
        target = os.path.join(dst, os.path.relpath(path, python_dir))
        os.makedirs(os.path.dirname(target), exist_ok=True)
        shutil.copy(path, target)
