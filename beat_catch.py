import librosa


def beat_times(audio_file):
    y, sr = librosa.load(audio_file)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    # 获取每个鼓点的时间（以秒为单位）
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    return beat_times


if __name__ == '__main__':
    pass
