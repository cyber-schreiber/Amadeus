"""Fills the default/empty Frames of Loop's bass attribute ~

These include 'rhythm', 'ints', 'notes', and 'final' ~
"""

from bass_write import *


def construct_bass(curr_loop):
    """Constructs Frames for the values in curr_loop's bass attribute dictionary ~
    This is a mutating function ~

    @type curr_loop: Loop
    @rtype: None
    """

    # First filling the rhythm Frame
    for i, curr_measure in enumerate(curr_loop.bass['rhythm'].measures):
        bass_rhythm(curr_measure, curr_loop)

    # Next filling the ints Frame
    curr_loop.bass['ints'] = curr_loop.bass['rhythm'].extend().collapse(curr_loop)
    for curr_measure in curr_loop.bass['ints'].measures:
        bass_notes(curr_measure, curr_loop)

    # Filling the notes Frame
    curr_loop.bass['notes'] = curr_loop.melody['ints'].extend().collapse(curr_loop)
    for curr_measure in curr_loop.bass['notes'].measures:
        for curr_note in curr_measure.notes:

            if curr_loop.bass['rhythm'][curr_note.index] == 'S':  # sustained note
                curr_note.value = curr_note.prev.value

            else:  # new note / attack
                curr_chord = curr_loop.harm['passing'][curr_note.index].value['chord']

                tonic = key_sharp_or_flat(curr_loop.key).index(curr_loop.key['root'])
                target = (tonic + curr_note.value + curr_chord.interval) % 12

                curr_note.value = chord_sharp_or_flat(curr_chord, curr_loop)[target]

    # Filling the final Frame
    curr_loop.bass['final'] = curr_loop.bass['notes'].extend().collapse(curr_loop)
    curr_loop.bass['final'].compress()
