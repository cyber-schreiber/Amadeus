"""Assigns rhythm and notes to the bass ~ """

import random
from melody_notes import *


def bass_rhythm(curr_measure, curr_loop):
    """Assigns rhythm values of 'A' (attack) or 'S' (sustain) to note values ~
    This is a mutating function ~

    @type curr_measure: Measure
    @type curr_loop: Loop
    @rtype: None
    """

    for i, curr_note in enumerate(curr_measure.notes):

        # First note of measure is attack -> may be improved, this is less clear for bass
        if i == 0:
            curr_note.value = 'A'

        # When a new chord plays, bass plays (root)
        elif curr_loop.harm['rhythm'][curr_note.index].value == 'A':
            curr_note.value = 'A'

        # Bass will probably attack spots marked 'salient' by rhythm_ref
        elif curr_loop.rhythm_ref[i] == 1 and random.randint(0, 2) != 0:
            curr_note.value = 'A'

        # Quarter notes have a chance of being attacked by bass
        elif i % 2 == 0 and random.randint(0, 2) == 0:
            curr_note.value = 'A'

        # Everything else is sustain
        else:
            curr_note.value = 'S'


def bass_notes(curr_measure, curr_loop):
    """Determines note values in integer form for a Measure of a Loop's melody 'ints' Frame

    @type curr_measure: Measure
    @type curr_loop: Loop
    @rtype: None
    """

    for i, curr_note in enumerate(curr_measure.notes):
        chord_scale = get_chord_scale(curr_loop.harm['passing'][i].value['chord'], curr_loop)

        if curr_note.value == 'A':

            # First bass note for new chord will be root -> this may be improved to include inversions
            if curr_loop.harm['rhythm'][curr_note.index].value == 'A':
                curr_note.value = 0
            else:
                curr_note.value = random.choice(chord_scale['shell'] + chord_scale['shell'] + chord_scale['guide']
                                                + chord_scale['color'])

        elif curr_note.value == 'S':
            curr_note.value = curr_note.prev.value

        else:  # curr_note.value == 'R'
            curr_note.value = -1
