import threading
import tkinter as tk
import wave
from tkinter import messagebox

import pyaudio
from PIL import Image, ImageTk, ExifTags

from beat_catch import beat_times


class WindowsShow:
    def __init__(self, root):
        self.data = []
        self.images = []
        self.current_image = None
        self.current_image_index = 0
        self.audio_path = None
        self.root = root
        self.stop_play = False

        self.image_label = tk.Label(root)
        self.image_label.pack()
        self.image_label.bind("<Double-Button-1>", self._stop_play)
        self.image_label.bind("<Button-1>", self.toggle_fullscreen)
        self.button_img = tk.Button(root, text="加载图片", command=self.load_image)
        self.button_img.pack()
        self.button_audio = tk.Button(root, text="加载音频", command=self.load_audio)
        self.button_audio.pack()
        self.button_start = tk.Button(root, text="开始", command=self.start_play)
        self.button_start.pack()
        self.button_stop = tk.Button(root, text="停止", command=self._stop_play)
        self.button_stop.pack()
        self.button_full = tk.Button(root, text="全屏", command=self.toggle_fullscreen)
        self.button_full.pack()

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"{screen_width}x{screen_height}")

    def _stop_play(self, *args):
        self.stop_play = True

    def load_image(self):
        file_path = self.ask_file_path()

        def load_task():
            for f in file_path:
                image = Image.open(f)

                # 检查是否包含 Exif 信息
                try:
                    for orientation in ExifTags.TAGS.keys():
                        if ExifTags.TAGS[orientation] == 'Orientation':
                            exif = dict(image.getexif())

                            if exif[orientation] == 3:
                                image = image.rotate(180, expand=True)
                            elif exif[orientation] == 6:
                                image = image.rotate(270, expand=True)
                            elif exif[orientation] == 8:
                                image = image.rotate(90, expand=True)
                except (AttributeError, KeyError, IndexError):
                    # 图像没有 Exif 信息，或者信息不完整
                    pass

                # 设置目标分辨率为1080p
                target_resolution = (self.root.winfo_screenwidth(), self.root.winfo_screenheight())

                # 使用thumbnail方法调整图像大小，保持纵横比不变
                image.thumbnail(target_resolution)
                photo = ImageTk.PhotoImage(image)
                self.images.append(photo)

        threading.Thread(target=load_task).start()

    def toggle_fullscreen(self, *args):
        # 获取当前窗口状态
        state = self.root.attributes('-fullscreen')

        # 切换全屏状态
        self.root.attributes('-fullscreen', not state)

    def load_audio(self):
        file_path = self.ask_file_path(True)
        self.audio_path = file_path
        threading.Thread(target=self.load_audio_data, args=[file_path]).start()

    def start_play(self):
        if not self.audio_path or self.data.__len__() == 0:
            messagebox.showinfo("提示", "未加载音频或者图片")
            return
        self.root.configure(bg="black")
        self.image_label.configure(bg="black")
        self.image_label.pack(before=self.button_img)
        self.stop_play = False
        global img_len, data_len
        img_len = len(self.images)
        data_len = len(self.data)

        def play():
            global img_len, data_len
            for t in self.play_audio(self.audio_path):
                if self.stop_play:
                    break
                if img_len > 0 and t >= self.data[self.current_image_index % data_len]:
                    self.current_image_index += 1
                    if self.current_image_index >= data_len:
                        continue
                    self.set_image(self.images[self.current_image_index % img_len])
                    img_len = len(self.images)
                    data_len = len(self.data)
            self.image_label.pack_forget()
            self.current_image_index = 0
            self.image_label.config(bg="white")
            self.root.config(bg="white")

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

    def load_audio_data(self, file):
        if file:
            self.data = []
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
