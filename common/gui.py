# generate from base common code
import tkinter as tk
import tkinter.messagebox
from tkinter import filedialog
from tkinter import simpledialog
from tkinter.ttk import Progressbar
import sys
import threading
import time
from typing import Any
from common import python_box
def message():
    global root
    root = _top()
    return tkinter.messagebox
def _top():
    global root
    win = root if root else tkinter.Tk()
    win.withdraw()
    return win
def select_dir(title="选择路径", use_argv=None):
    global root
    if use_argv:
        if len(sys.argv) > use_argv:
            return sys.argv[use_argv]
    root = _top()
    return filedialog.askdirectory(title=title)
class ComWin:
    def __init__(self, root: tkinter.Tk = None, width: int = None, height: int = None, title=None):
        self.root = root  # type: tkinter.Tk
        self.back_loop()
        self.width = width if width else int(self.root.winfo_screenwidth() * 0.5)
        self.height = height if height else int(self.root.winfo_screenheight() * 0.5)
        # 创建一个Canvas组件，设置宽度为屏幕宽度的一半撑开窗口宽度
        canvas = tk.Canvas(self.root, width=self.width, height=1)
        canvas.pack()
        if title:
            self.root.title(title)

    def _mainloop(self):
        self.root = self.root if self.root else tkinter.Tk()
        self.root.mainloop()

    def back_loop(self):
        python_box.thread_runner(lambda: self._mainloop())
        for i in range(50):
            if self.root:
                break
            time.sleep(0.1)

    def resize(self, width: int = None, height: int = None):
        self.root.geometry(
            f"{width if width else int(self.root.winfo_screenwidth() * 0.5)}x{height if height else int(self.root.winfo_screenheight() * 0.5)}")

    def add_text(self, text) -> tk.Label:
        # 创建一个Label组件并将其添加到self.root上
        label = tk.Label(self.root, text=text)
        label.pack()
        return label

    def add_buton(self, title="按钮", on_button_click_callback=None) -> tk.Button:
        global root
        # 创建一个按钮，并将on_button_click函数绑定到按钮的点击事件
        button = tk.Button(self.root, text=title, command=on_button_click_callback)
        button.pack()
        return button