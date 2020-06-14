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
# ##################################################
# python file importing
# ##################################################
from modules.err import ChordSyntaxError, NotesCharacterError
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

    def notes_to_chord(self, data: list, root: int = None) -> list:
        """
        To return chord letters (for triad, seventh and ninth)

        :return: list
        """
        # TODO: use chord_dict.json for notes_to_chord()

        elements_num = len(data)

        # chord appropriateness check
        if elements_num < 3:
            return []

        if elements_num > 5:
            return []

        # constant data
        if elements_num == 3:
            chord_set = [[0, 4, 7], [0, 3, 7], [0, 3, 6], [0, 4, 8], [0, 5, 7], [0, 4, 6]]
            chord_name = {0: '', 1: 'm', 2: 'dim', 3: 'aug', 4: 'sus4', 5: '-5', -1: ''}

        elif elements_num == 4:
            chord_set = [[0, 4, 7, 10], [0, 4, 7, 11], [0, 3, 7, 10], [0, 3, 7, 11],
                         [0, 3, 6, 10], [0, 3, 6, 9], [0, 4, 8, 11], [0, 5, 7, 10],
                         [0, 4, 7, 9], [0, 3, 7, 9], [0, 2, 4, 7], [0, 4, 5, 7],
                         [0, 4, 6, 10], [0, 4, 8, 10], [0, 3, 6, 11]]
            chord_name = {0: '7', 1: 'M7', 2: 'm7', 3: 'mM7', 4: 'm7-5', 5: 'dim7', 6: 'augM7', 7: '7sus4',
                          8: '6', 9: 'm6', 10: '(add9)', 11: '(add4)', 12: '7-5', 13: 'aug7', 14: 'dimM7', -1: ''}

        else:
            chord_set = [[0, 2, 4, 7, 10], [0, 1, 4, 7, 10], [0, 3, 4, 7, 10], [0, 4, 5, 7, 10], [0, 3, 5, 7, 10],
                         [0, 4, 6, 7, 10], [0, 4, 6, 7, 11], [0, 4, 7, 9, 10], [0, 4, 7, 8, 10], [0, 2, 4, 7, 9],
                         [0, 2, 3, 7, 9], [0, 2, 4, 6, 10], [0, 1, 4, 8, 10], [0, 2, 4, 8, 10], [0, 2, 3, 7, 10]]
            chord_name = {0: '9', 1: '7(b9)', 2: '7(b10)', 3: '7(11)', 4: 'm7(11)', 5: '7(#11)', 6: 'M7(#11)',
                          7: '7(13)', 8: '7(b13)', 9: '69', 10: 'm69', 11: '9-5', 12: 'aug7-9', 13: 'aug9',
                          14: 'm9', -1: ''}

        tmp = sorted(data.copy())
        ans = []

        # each elements assume the root
        for trs in range(elements_num):
            root_tmp = tmp[trs]
            tmp_1 = list(map(lambda x: (x - root_tmp) % 12, tmp))
            tmp_1 = sorted(tmp_1)

            # search chords
            for i, j in enumerate(chord_set):
                if j == tmp_1:
                    # slash code
                    if root is not None and root != root_tmp:
                        ans.append('{}{}/{}'.format(self.ntoc[root_tmp], chord_name[i], self.ntoc[root]))
                        break

                    else:
                        ans.append('{}{}'.format(self.ntoc[root_tmp], chord_name[i]))
                        break

        return ans

    def chord_to_notes(self, chord: str) -> dict:
        """
        To return notes which construct a given chord letter
        :param chord: chord letter you want to analyze
        :return: dict
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
        with open('chord_dict.json', mode='r', encoding='utf-8') as f:
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
        elem = list(map(lambda x: self.ntoc[x], elem))

        # return
        if chord_bass is not None:
            return {'chord': chord, 'main': elem, 'bass': chord_bass}
        else:
            return {'chord': chord, 'main': elem, 'bass': root_char}


if __name__ == '__main__':
    pass
