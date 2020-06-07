# coding: utf-8
# !/usr/bin/env python3
# ##################################################
#
# 2020/06/02
# written by: Apoi
# version: 0.1.1
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

# ##################################################
# python file importing
# ##################################################

# ##################################################
# class
# ##################################################


class ChordLetters(object):
    """
    To return the chord letters from the given notes
    """
    def __init__(self, data: list, root: int = None, sharp: bool = False, *args, **kwargs):

        # Correspondence between pitches and numbers
        if sharp:
            self.ntoc = {0: 'C', 1: 'C#', 2: 'D', 3: 'D#', 4: 'E', 5: 'F',
                         6: 'F#', 7: 'G', 8: 'G#', 9: 'A', 10: 'A#', 11: 'B', -1: ''}
        else:
            self.ntoc = {0: 'C', 1: 'Db', 2: 'D', 3: 'Eb', 4: 'E', 5: 'F',
                         6: 'Gb', 7: 'G', 8: 'Ab', 9: 'A', 10: 'Bb', 11: 'B', -1: ''}

        self.cton = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4,  'F': 5, 'F#': 6,
                     'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11, '': -1}

        # init the others
        self.data = data
        self.root = root
        self.args = args
        self.kwargs = kwargs

    def notes_to_chord(self) -> list:
        """
        To return the chord letters (for triad, seventh and ninth)

        :return: list
        """

        elements_num = len(self.data)

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
                         [0, 4, 6, 10], [0, 4, 8, 10]]
            chord_name = {0: '7', 1: 'M7', 2: 'm7', 3: 'mM7', 4: 'm7-5', 5: 'dim7', 6: 'M7+5', 7: '7sus4',
                          8: '6', 9: 'm6', 10: '(add9)', 11: '(add4)', 12: '7-5', 13: 'aug7', -1: ''}

        else:
            chord_set = [[0, 2, 4, 7, 10], [0, 1, 4, 7, 10], [0, 3, 4, 7, 10], [0, 4, 5, 7, 10], [0, 3, 5, 7, 10],
                         [0, 4, 6, 7, 10], [0, 4, 6, 7, 11], [0, 4, 7, 9, 10], [0, 4, 7, 8, 10], [0, 2, 4, 7, 9],
                         [0, 2, 3, 7, 9]]
            chord_name = {0: '9', 1: '7(b9)', 2: '7(b10)', 3: '7(11)', 4: 'm7(11)', 5: '7(#11)', 6: 'M7(#11)',
                          7: '7(13)', 8: '7(b13)', 9: '69', 10: 'm69', -1: ''}

        tmp = sorted(self.data.copy())
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
                    if self.root is not None and self.root != root_tmp:
                        ans.append('{}{}/{}'.format(self.ntoc[root_tmp], chord_name[i], self.ntoc[self.root]))
                        break

                    else:
                        ans.append('{}{}'.format(self.ntoc[root_tmp], chord_name[i]))
                        break

        return ans


if __name__ == '__main__':
    data = list(map(int, input().split()))
    root = None
    cl = ChordLetters(data, root, sharp=False)
    print(cl.notes_to_chord())
