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
        if transpose < -11 or 11 < transpose:
            raise ValueError('\'transpose\' should be between -11 and 11.')

        if pitch < 410 or 494 < pitch:
            raise ValueError('\'pitch\' should be between 410 and 494.')

        if not re.fullmatch(r'.+?\.wav$', title):
            title += '.wav'

        # wave initialization
        wave = SoundGenerator.oscillator(0, sec, sampling_rate)

        # elements' frequencies
        # fn is a num the one before
        fn = -1

        # wave synthesize
        for i in sound:
            if fn >= i:
                # 15 = 12(octave) + 3(C base-> A base convert)
                f = pitch * 2 ** ((15 + i) / 12)
            else:
                f = pitch * 2 ** ((3 + i) / 12)

            wave += SoundGenerator.oscillator(f, sec, sampling_rate)

            # memory a number the one before
            fn = i

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

    def create(self, sound, *args,
               inversion: int = 0,
               single_tone: bool = False,
               with_bass: bool = False,
               bass_note: int = -1,
               transpose: int = 0,
               octave: int = 0,
               pitch: float = 440.0,
               sec: float = 5.0,
               sampling_rate: int = 441000,
               volume_adjustment: (str, float) = 'auto',
               title: str = 'sound.wav',
               at: str = None
               ):
        """
        To manage sound creation

        :param sound: sound note(s), chord symbol you want to create
        :param args: DO NOT USE this param, info in this param will be ignored.
        :param inversion: root -> 0, first to fourth inversion -> 1 to 4
        :param single_tone: It should be True when a letter in param 'sound' is a single tone, not a chord.
        :param with_bass: It should be True when bass sound is also needed.
        :param bass_note: If param 'with_bass' is True, bass sound in this param will be added.
        :param transpose: A value of transposing can be set. The value must be between -11 and 11.
        :param octave: A value of octave transposing (= transpose +-12) can be set.
        :param pitch: mid A's pitch
        :param sec: length of wave
        :param sampling_rate: wave sampling rate. If you are not a sound engineer, default value is recommended.
        :param volume_adjustment: preventing sound cracking. 'auto'(default) is recommended.
        :param title: wave file's title. If 'title' does not end with '.wav', '.wav' is automatically added.
        :param at: specifying wave file's path
        :return: None (wave file is created.)
        """

        # kwargs control
        data = {'inversion': inversion,
                'single_tone': single_tone,
                'with_bass': with_bass,
                'bass_note': bass_note,
                'transpose': transpose,
                'octave': octave,
                'pitch': pitch,
                'sec': sec,
                'sampling_rate': sampling_rate,
                'volume_adjustment': volume_adjustment,
                'title': title,
                'at': at,
                'others': args}

        # data sanitization
        if isinstance(data['bass_note'], str):
            data['bass_note'] = self.cton[data['bass_note']]

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
