"""Contains rhythm algorithms for melody and bass ~ """

import random


def assign_rests(curr_measure, curr_loop):
    """Assigns rests for a 4/4 measure ~
    This is a mutating function ~

    @type curr_loop: Loop
    @type curr_measure: Measure
    @rtype: None
    """

    rest_amount = random.randint(0, 3)
    rest_count = 0

    while rest_count < rest_amount:
        for i, curr_note in enumerate(curr_measure.notes):

            # Adding rests at random positions, if the position is not marked 'salient' by rhythm_ref
            if curr_note.value is None and random.randint(0, 10) == 0 and curr_loop.rhythm_ref[i] != 1:
                curr_note.value = 'R'
                rest_count += 1

            # Adding rests adjacent to rests already added
            if curr_note.value == 'R' and random.randint(0, 4) == 0 and i != len(curr_measure.notes)-1:
                if curr_loop.rhythm_ref[i+1] != 1 and random.randint(0, 2) > 0:
                    curr_note.next.value = 'R'
                    rest_count += 1

            if curr_note.value == 'R' and random.randint(0, 4) == 0 and i != 0:
                if curr_loop.rhythm_ref[i-1] != 1 and random.randint(0, 2) > 0:
                    curr_note.prev.value = 'R'
                    rest_count += 1

            if rest_count == rest_amount:
                return


def melody_rhythm(curr_measure, curr_loop):
    """Assigns rhythm values of 'A' (attack) or 'S' (sustain) to remaining note values ~
    This is a mutating function ~

    @type curr_measure: Measure
    @type curr_loop: Loop
    @rtype: None
    """

    for i, curr_note in enumerate(curr_measure.notes):
        if curr_note.value != 'R':

            # Every measure starts with an attack -> this can DEFINITELY be improved
            if i == 0:
                curr_note.value = 'A'

            # Attack follows a rest
            elif curr_note.prev.value == 'R':
                curr_note.value = 'A'

            # Spots marked 'salient' by rhythm_ref have high chance to be attack
            elif curr_loop.rhythm_ref[i] == 1 and random.randint(0, 2) != 0:
                curr_note.value = 'A'

            # Everything else is sustain
            else:
                curr_note.value = 'S'
