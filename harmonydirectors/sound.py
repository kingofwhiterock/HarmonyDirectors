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

    def _create(self):
        pass

    def create(self, sound, *,
               single_tone: bool = False,
               with_bass: bool = False,
               transpose: int = 0,
               octave: int = 0,
               pitch: int = 440,
               sec: float = 5.0,
               sampling_rate: int = 441000,
               volume_adjustment: (str, float) = 'auto',
               title: str = 'sound.wav',
               ):
        if isinstance(sound, str):
            pass


if __name__ == '__main__':
    pass
