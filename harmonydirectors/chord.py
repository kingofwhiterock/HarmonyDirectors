# coding: utf-8
# !/usr/bin/env python3
# ##################################################
#
# 2020/06/02
# written by: Apoi
# version: 0.2.0
#
# ##################################################
#
# PROJECT:
# HarmonyDirectors
#
# FILE PURPOSE:
# TO RETURN THE CHORD LETTERS
#
# FILE ISSUE:
# NONE
#
# ##################################################

# ##################################################
# library importing
# ##################################################
import json
import sys
# ##################################################
# python file importing
# ##################################################
from harmonydirectors.err import ChordSyntaxError, NotesCharacterError
# ##################################################
# class
# ##################################################


class ChordLetters(object):
    """
    To return chord letters from the given notes
    """
    def __init__(self, sharp: bool = False, *args, **kwargs):

        # Correspondence between pitches and numbers
        if sharp:
            self.ntoc = {0: 'C', 1: 'C#', 2: 'D', 3: 'D#', 4: 'E', 5: 'F',
                         6: 'F#', 7: 'G', 8: 'G#', 9: 'A', 10: 'A#', 11: 'B', -1: ''}
        else:
            self.ntoc = {0: 'C', 1: 'Db', 2: 'D', 3: 'Eb', 4: 'E', 5: 'F',
                         6: 'Gb', 7: 'G', 8: 'Ab', 9: 'A', 10: 'Bb', 11: 'B', -1: ''}

        self.cton = {'Cb': 11, 'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3,
                     'E': 4, 'E#': 5, 'Fb': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7,
                     'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11, 'B#': 0, '': -1}

        # init the others
        self.args = args
        self.kwargs = kwargs

    def _chord_to_elem(self, chord: str) -> tuple:
        """
        To return notes which construct a given chord letter

        Used to SoundGenerator, chord_to_ notes()

        :param chord: chord letter you want to analyze
        :return: tuple
        """
        # search root and calc transpose
        root_char = chord[0]
        try:
            dif = self.cton[root_char]
        except KeyError:
            raise ChordSyntaxError('\'%s\' is an invalid chord symbol.' % chord)

        if len(chord) > 1:
            half_note = chord[1]
            if half_note == '#' or half_note == 'b':
                root_char += half_note
                dif = self.cton[root_char]

        # search bass
        tmp = chord.split('/')
        if len(tmp) == 1:
            chord_main = tmp[0]
            chord_bass = None
        elif len(tmp) == 2:
            chord_main = tmp[0]
            chord_bass = tmp[1]
        else:
            raise ChordSyntaxError('\'%s\' is an invalid chord symbol.' % chord)

        # load chord_dict.json
        tmp = sys.path[-1] + '/harmonydirectors/const/chord_dict.json'
        with open(tmp, mode='r', encoding='utf-8') as f:
            cd = json.load(f)

        # searching
        elem = None
        for t in ['triad', 'seventh', 'ninth']:
            for name, elem in cd[t].items():
                if root_char + name == chord_main:
                    break
            else:
                continue
            break
        else:
            elem = []

        # convert elements -> note chars
        elem = list(map(lambda x: (x + dif) % 12, elem))

        # return
        if chord_bass is not None:
            return elem, self.cton[chord_bass], dif
        else:
            return elem, chord_bass, dif

    def char_to_array(self, data: (str, list)) -> list:
        """
        To convert a pitch name into array data
        :param data: a pitch name (str or list)
        :return: list
        """
        if type(data) == str:
            try:
                return [self.cton[data]]
            except KeyError:
                raise NotesCharacterError('\'%s\' can\'t be used.' % data)

        if type(data) == list:
            tmp = []
            for i in data:
                try:
                    tmp.append(self.cton[i])
                except KeyError:
                    raise NotesCharacterError('\'%s\' can\'t be used.' % i)
            return tmp

        raise TypeError('param must be \'str\' or \'list\'')

    def chord_to_notes(self, chord: str) -> dict:
        """
        To return notes which construct a given chord letter
        :param chord: chord letter you want to analyze
        :return: dict
        """
        # get elem and bass
        elem, chord_bass, root_char = self._chord_to_elem(chord)

        # convert elements -> note chars
        elem = list(map(lambda x: self.ntoc[x], elem))

        # return
        if chord_bass is not None:
            return {'chord': chord, 'main': elem, 'bass': chord_bass}
        else:
            return {'chord': chord, 'main': elem, 'bass': root_char}

    def notes_to_chord(self, data: list, root: int = None) -> list:
        """
        To return chord letters (for triad, seventh and ninth)

        :return: list
        """

        elements_num = len(data)

        # chord appropriateness check
        if elements_num < 3:
            return []

        if elements_num > 5:
            return []

        # load json
        with open('const/chord_dict.json', mode='r', encoding='utf-8') as f:
            raw = json.load(f)

        # constant data
        if elements_num == 3:
            chord_set: dict = raw['triad']

        elif elements_num == 4:
            chord_set: dict = raw['seventh']

        else:
            chord_set: dict = raw['ninth']

        chord_set = {i: sorted(x) for i, x in chord_set.items()}
        tmp = sorted(data.copy())
        ans = []

        # each elements assume the root
        for trs in tmp:
            root_tmp = trs
            tmp_1 = list(map(lambda x: (x - root_tmp) % 12, tmp))
            tmp_1 = sorted(tmp_1)

            # search chords
            for i, j in chord_set.items():
                if j == tmp_1:
                    # slash code
                    if root is not None and root != root_tmp:
                        ans.append('{}{}/{}'.format(self.ntoc[root_tmp], i, self.ntoc[root]))
                        break

                    else:
                        ans.append('{}{}'.format(self.ntoc[root_tmp], i))
                        break

        return ans


if __name__ == '__main__':
    pass
