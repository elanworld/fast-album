import threading
import tkinter as tk
import wave

import pyaudio
from PIL import Image, ImageTk

from beat_catch import beat_times


class WindowsShow:
    def __init__(self, root):
        self.data = []
        self.images = []
        self.current_image = None
        self.root = root
        self.image_label = tk.Label(root)
        self.image_label.pack(expand=True, fill="both")

        self.load_button = tk.Button(root, text="Load Image", command=self.load_image)
        self.load_button.pack()
        self.load_button = tk.Button(root, text="Load Audio", command=self.load_audio)
        self.load_button.pack()
        self.root.bind("<Configure>", self.on_window_resize)

    def on_window_resize(self, event):
        new_width = event.width


    def load_image(self):
        file_path = self.ask_file_path()
        for f in file_path:
            image = Image.open(f)
            # 设置目标分辨率为1080p
            target_resolution = (1920, 1080)

            # 使用thumbnail方法调整图像大小，保持纵横比不变
            image.thumbnail(target_resolution)
            photo = ImageTk.PhotoImage(image)
            self.images.append(photo)

    def load_audio(self):
        file_path = self.ask_file_path(True)
        self.input_file(file_path)
        p = self

        def play():
            for t in p.play_audio(file_path):
                if len(p.images) > 0:
                    p.set_image(p.images[int(t) % len(p.images)])

        threading.Thread(target=play).start()

    def update(self):
        self.root.update()

    def set_image(self, photo):
        if photo == self.current_image:
            return
        self.current_image = photo
        self.image_label.config(image=photo)
        self.image_label.image = photo  # 保持对图片的引用

    def ask_file_path(self, audio=False):
        from tkinter import filedialog
        if audio:
            return filedialog.askopenfilename(title="Select an Image",
                                              filetypes=[("Image files", "*.wav")], )

        file_path = filedialog.askopenfilenames(
            title="Select an Image",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")],
        )
        return file_path

    def input_file(self, file):
        self.data = beat_times(file)

    def play_audio(self, file_path):
        chunk = 1024  # 设置缓冲区大小
        wf = wave.open(file_path, 'rb')  # 打开音频文件

        # 初始化 PyAudio
        p = pyaudio.PyAudio()
        stream = p.open(
            format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True
        )
        play_process = 0
        data = wf.readframes(chunk)
        # 播放音频
        while data:
            play_process += chunk / wf.getframerate()
            yield play_process
            stream.write(data)
            data = wf.readframes(chunk)

        stream.stop_stream()
        stream.close()
        p.terminate()


if __name__ == '__main__':
    root = tk.Tk()
    show = WindowsShow(root)
    root.mainloop()
