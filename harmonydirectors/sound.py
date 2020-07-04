# coding: utf-8
# !/usr/bin/env python3
# ##################################################
#
# 2020/06/02
# written by: Apoi
# version: 0.1.0
#
# ##################################################
#
# PROJECT:
#
#
# FILE PURPOSE:
#
#
# FILE ISSUE:
#
#
# ##################################################

# ##################################################
# library importing
# ##################################################
import numpy as np
from scipy.io import wavfile
import re
# ##################################################
# python file importing
# ##################################################
from harmonydirectors.chord import ChordLetters
# ##################################################
# class
# ##################################################


class SoundGenerator(ChordLetters):
    """
    To generate harmony of given note(s)

    SoundGenerator is a subclass of ChordLetters.
    """
    def __init__(self):
        super(SoundGenerator, self).__init__()

    @staticmethod
    def oscillator(freq: float, sec: float, rate: int = 441000):
        """
        To generate sine wave array
        
        :param freq: frequency
        :param sec: wave length (seconds)
        :param rate: sampling rate (non-developer should NOT change the value)
        :return: nparray (sine wave)
        """
        phases = np.cumsum(2.0 * np.pi * freq / rate * np.ones(int(rate * sec)))
        return np.sin(phases)

    def _create(self, sound: (list, tuple), data: dict):
        """
        To generate a wave file of specified sound

        :param sound: should be a list or a tuple. Each numbers should be between 0 to 12 but sanitation will be done.
        :param data: should be a dict. See self.create() and docs.
        :return: None (wave file is generated in current directory or in specified directory)
        """
        # data substitution
        # TODO: use other params
        inversion: int = data['inversion']
        single_tone: bool = data['single_tone']
        with_bass: bool = data['with_bass']
        bass_note: int = data['bass_note']
        transpose: int = data['transpose']
        octave: int = data['octave']
        pitch: float = data['pitch']
        sec: float = data['sec']
        sampling_rate: int = data['sampling_rate']
        volume_adjustment: (str, float) = data['volume_adjustment']
        title: str = data['title']
        at: str = data['at']

        # data sanitization
        if pitch < 410 or 494 < pitch:
            raise ValueError('\'pitch\' should be between 410 and 494.')

        if not re.fullmatch(r'.+?\.wav$', title):
            title += '.wav'

        # elements' frequencies
        # fn is a num the one before
        fn = -1

        # wave init
        wave = SoundGenerator.oscillator(0, sec, sampling_rate)

        # wave synthesize
        for i in sound:
            if fn >= i:
                # 15 = 12(octave) + 3(C base-> A base convert)
                f = pitch * 2 ** ((15 + i) / 12)
            else:
                f = pitch * 2 ** ((3 + i) / 12)
            wave += SoundGenerator.oscillator(f, sec, sampling_rate)

        # volume controlling
        if volume_adjustment == 'auto':
            wave *= 0.1
        elif isinstance(volume_adjustment, (int, float)):
            wave *= volume_adjustment
        else:
            ValueError('\'volume_adjustment\' should be \'auto\' or float.')

        # wave convert
        wave = (wave * float(2 ** 15 - 1)).astype(np.int16)

        # make wave_file
        wavfile.write(title, sampling_rate, wave)

    def create(self, sound, **kwargs):
        """
        To manage sound creation

        :param sound: note character(s) or chord letters

        :param kwargs: Some parameters can be used.
                       See docs and check available parameters and their default values.

        :return: None (wave file is generated in current directory or in specified directory)
        """
        # kwargs control
        data = {'inversion': 0,
                'single_tone': False,
                'with_bass': False,
                'bass_note': -1,
                'transpose': 0,
                'octave': 0,
                'pitch': 440.0,
                'sec': 5.0,
                'sampling_rate':  441000,
                'volume_adjustment': 'auto',
                'title': 'sound.wav',
                'at': None}

        for k, v in kwargs.items():
            if k == 'bass_note' and isinstance(v, str):
                data[k] = self.cton[v]
            else:
                data[k] = v

        # param sound check
        if isinstance(sound, str):
            if data['single_tone']:
                self._create([self.cton[sound]], data)
            else:
                self._create(self._chord_to_elem(sound)[0], data)

        elif isinstance(sound, int):
            data['single_tone'] = True
            self._create([sound], data)

        elif isinstance(sound, (list, tuple)):
            try:
                if isinstance(sound[0], str):
                    sound = list(map(lambda x: self.cton[x], sound))
                    self._create(sound, data)

                elif isinstance(sound[0], int):
                    self._create(sound, data)
            except IndexError:
                if data['with_bass'] and data['bass_note'] != '':
                    self._create(sound, data)
                else:
                    pass

        else:
            raise TypeError('An invalid parameters is used.')


if __name__ == '__main__':
    pass
