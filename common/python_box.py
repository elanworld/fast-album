# generate from base common code
import os
import collections
import datetime
import io
import logging
import string
import threading
import time
from typing import Union, AnyStr, Optional
from typing.io import IO
import re
import ctypes
import platform
def dir_list(directory=None, filter_str="", return_full_path=True, walk=False, return_dir=False):
    if directory is None:
        directory = "."
    if os.path.exists(directory):
        if os.path.isfile(directory):
            return [directory]
    else:
        return []
    file_list = []
    for path, dirs, files in os.walk(directory):
        for file in files:
            if return_full_path:
                filepath = os.path.join(os.path.abspath(path), file)
            else:
                filepath = os.path.relpath(os.path.join(os.path.abspath(path), file), directory)
            file_list.append(filepath)
        if return_dir:
            for dire in dirs:
                if return_full_path:
                    filepath = os.path.join(os.path.abspath(path), dire)
                else:
                    filepath = os.path.relpath(os.path.join(os.path.abspath(path), dire), directory)
                file_list.append(filepath)
        if walk is False:
            break
    if filter_str:
        for i in range(len(file_list) - 1, -1, -1):
            if not re.search(filter_str, file_list[i]):
                file_list.remove(file_list[i])
    return file_list
def write_file(text_list, file="text.txt", append=False):
    _mk_file_dir(file)
    mode = 'a' if append else 'w'
    if type(text_list) == list:
        with open(file, mode, encoding="utf-8") as f:
            for line in text_list:
                f.write(line + "\n")
    if type(text_list) == str:
        with open(file, mode, encoding="utf-8") as f:
            f.writelines(text_list)
def _mk_file_dir(file):
    dirname = os.path.dirname(file)
    if dirname and not os.path.exists(dirname):
        os.makedirs(dirname, exist_ok=True)