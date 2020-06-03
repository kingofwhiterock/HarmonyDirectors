# coding: utf-8
# library importing
import matplotlib.pyplot as plt
import numpy as np
import wave
import struct


# definition
def create_wave(a, fs, f0, t):
    point = np.arange(0, fs * t)
    sin_wave = a * np.sin(2 * np.pi * f0 * point / fs)

    return sin_wave


def superimpose_wave(wv0, wv1):
    # 16bit符号付整数に変換
    wv0 = [int(x * 32767.0) for x in wv0]
    wv1 = [int(x * 32767.0) for x in wv0]
    print(type(wv0))
    # 重ね合わせ
    wv_tmp = [(wv0[x] + wv1[x]) // 100000 for x in range(len(wv0))]
    print(wv_tmp[0: 100])
    plt.plot(wv_tmp)
    # plt.show()
    return wv_tmp


def binary_wave(tmp):
    # バイナリ化
    binwave = struct.pack('h' * len(tmp), *tmp)
    return binwave


# parameters
a = 1  # 振幅
fs = 44100  # サンプリング周波数
f0 = 442 * 2 ** (0 / 12)  # 基本周波数
f1 = 442 * 2 ** (7 / 12)  # 基本周波数
f2 = 442 * 2 ** (4 / 12)  # 基本周波数
sec = 10  # 秒数


if __name__ == '__main__':
    s0 = create_wave(a, fs, f0, sec)
    s1 = create_wave(a, fs, f1, sec)
    s2 = create_wave(a, fs, f2, sec)
    print(type(s0))

    tt0 = superimpose_wave(s0, s1)
    # tt1 = superimpose_wave(tt0, s2)
    print(type(tt0))

    sound = binary_wave(tt0)

    with wave.Wave_write('sample.wav') as w:
        p = (1, 2, fs, len(sound), 'NONE', 'not compressed')
        w.setparams(p)
        w.writeframes(sound)
