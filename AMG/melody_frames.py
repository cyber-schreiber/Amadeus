"""Fills the default/empty Frames of Loop's melody attribute ~

These include 'rhythm', 'ints', 'notes', and 'final' ~
"""

from melody_rhythm import *
from melody_notes import *


def construct_melody(curr_loop):
    """Constructs Frames for the values in curr_loop's melody attribute dictionary ~
    This is a mutating function ~

    @type curr_loop: Loop
    @rtype: None
    """

    # First filling the rhythm Frame
    for i, curr_measure in enumerate(curr_loop.melody['rhythm'].measures):
        if i % 4 in [0, 3] or i == curr_loop.measures-1:  # AAAB CCCD EEEF etc pattern for rhythm repetition
            assign_rests(curr_measure, curr_loop)
            melody_rhythm(curr_measure, curr_loop)
        else:
            for i2, curr_note in enumerate(curr_measure.notes):
                curr_note.value = curr_measure.prev.notes[i2].value

    # Next filling the ints Frame
    curr_loop.melody['ints'] = curr_loop.melody['rhythm'].extend().collapse(curr_loop)
    for curr_measure in curr_loop.melody['ints'].measures:
        melody_notes(curr_measure, curr_loop)

    # Filling the notes Frame
    curr_loop.melody['notes'] = curr_loop.melody['ints'].extend().collapse(curr_loop)
    for curr_measure in curr_loop.melody['notes'].measures:
        for curr_note in curr_measure.notes:
            if curr_loop.melody['rhythm'][curr_note.index] == 'S':  # sustained note
                curr_note.value = curr_note.prev.value

            elif curr_note.value == -1:  # rest
                curr_note.value = 'r'

            else:  # new note / attack
                # print(curr_loop.harm['passing'])
                curr_chord = curr_loop.harm['passing'][curr_note.index].value['chord']

                tonic = key_sharp_or_flat(curr_loop.key).index(curr_loop.key['root'])
                target = (tonic + curr_note.value + curr_chord.interval) % 12

                curr_note.value = chord_sharp_or_flat(curr_chord, curr_loop)[target]

    # Filling the final Frame
    curr_loop.melody['final'] = curr_loop.melody['notes'].compress()
