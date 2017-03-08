"""Mutates Frame objects by adding melody values in integer form ~ """

from functions import *
import random


def melody_notes(curr_measure, curr_loop):
    """Determines note values in integer form for a Measure of a Loop's melody 'ints' Frame

    @type curr_measure: Measure
    @type curr_loop: Loop
    @rtype: None
    """

    for i, curr_note in enumerate(curr_measure.notes):
        # print(curr_loop.harm['passing'], i)
        chord_scale = get_chord_scale(curr_loop.harm['passing'][i].value['chord'], curr_loop)

        if curr_note.value == 'A':
            options = chord_scale['guide'] + chord_scale['shell'] + chord_scale['color']

            # Guide tones should be strongest, followed by shell, then color tones are weak
            if curr_note.index % 4 == 0:
                for _ in range(2):
                    options.extend(chord_scale['guide'])
            elif curr_note.index % 2 == 0:
                for _ in range(2):
                    options.extend(chord_scale['shell'])
            else:
                for _ in range(2):
                    options.extend(chord_scale['color'])

            # Give huge preference to notes closer to previous note
            prev_notes = [this.value for this in
                          curr_loop.melody['rhythm'].extend().measures[0].notes[:curr_note.index]]
            if 'A' in prev_notes:
                first_note = False
            else:  # as there are no previous attacks, this is the first note of the loop, i.e. there is no prev note
                first_note = True

            if not first_note:
                prev_note = curr_loop.melody['rhythm'][curr_note.index].prev

                while prev_note.value == 'R':
                    prev_note = prev_note.prev

                prev_note = curr_loop.melody['ints'][prev_note.index]

                for next_note in chord_scale['guide'] + chord_scale['shell'] + chord_scale['color']:
                    if prev_note.value == next_note:
                        continue

                    delta = min([abs(prev_note.value - next_note), 12-abs(prev_note.value - next_note)])

                    for _ in range((5 - delta) ** 2):
                        options.append(next_note)

            # Color tones should be avoided before rests
            next_notes = [this for this in curr_loop.melody['rhythm'].extend().measures[0].notes[curr_note.index+1:]]
            delete = False
            for next_note in next_notes:
                if next_note is None:
                    delete = True
                    break
                elif next_note.value == 'R':
                    delete = True
                    break
                elif next_note.value == 'A':
                    delete = False
                    break

            if delete:
                for color_tone in chord_scale['color']:
                    while color_tone in options:
                        options.remove(color_tone)
                options.extend(chord_scale['color'])  # so that there is still a small chance of color tone here

            curr_note.value = random.choice(options)

        elif curr_note.value == 'S':
            curr_note.value = curr_note.prev.value

        else:  # curr_note.value == 'R'
            curr_note.value = -1


def get_chord_scale(curr_chord, curr_loop):
    """Takes a chord and returns its guide tones, shell notes, and color tones

    @type curr_chord: Chord
    @type curr_loop: Loop
    @rtype: dictionary {'guide': [0, 7], ...}
    """

    chord_scale = {'guide': [], 'shell': [], 'color': []}

    if curr_chord.quality == 'major':
        chord_scale['guide'] = [4, 11]
        chord_scale['shell'] = [0, 7]
        chord_scale['color'] = [2, 6, 9]

        if curr_chord.name == 'Imaj':
            chord_scale['color'].remove(6)
        if curr_loop.attributes['depth'] >= 2:
            chord_scale['shell'].remove(0)

    elif curr_chord.quality == 'minor':
        chord_scale['guide'] = [3, 10]
        chord_scale['shell'] = [0, 7]
        chord_scale['color'] = [2, 5, 9]

        if curr_chord.name in ['II-', 'relII-', 'V-', 'I-']:
            chord_scale['color'].remove(9)
        if curr_chord.name == 'III-':
            chord_scale['color'].remove(2)
        if curr_chord.name == 'relII-7b5':
            chord_scale['shell'][1] = 6
            chord_scale['color'] = [5, 8]

    else:  # full_chords[spots.index(spot)].quality == 'dominant'
        chord_scale['guide'] = [4, 10]
        chord_scale['shell'] = [0, 7]
        chord_scale['color'] = [2, 9]

        if curr_chord.name == 'V7/II':
            chord_scale['color'] = [2, 8]
        elif curr_chord.name in ['V7/III', 'V7/VI'] or curr_chord.name == 'V7' and curr_loop.key['quality'] == 'minor':
            chord_scale['color'] = [1, 3, 8]

    return chord_scale
