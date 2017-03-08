"""Contains code for percussion"""

import random


def write_kicks(curr_measure, curr_loop):
    """Writes the kicks for a standard measure in Frame object 'curr_frame'

    @type curr_measure: Measure
    @type curr_loop: Loop
    @rtype: None
    """
    kicks = [10, 20, 30, 40, 50, 60, 70, 80]  # dummy values
    for count, kick in enumerate(kicks):
        # Increasing likelihood of hit if the beat has been marked for rhythmic coordination among instruments
        if curr_loop.rhythm_ref[count] == 1:
            add_val = 2
        else:
            add_val = 4

        if count == 0 or count == 4:
            kicks[count] = 1
        elif count != 2 and count != 6 and random.randint(0, add_val) < 2:
            kicks[count] = 1

    for i, kick in enumerate(kicks):
        if kick == 1:
            curr_measure.notes[i].value = 'kick'
        else:
            curr_measure.notes[i].value = 'rest'


def write_snares(curr_measure):
    """Writes the snares for a standard measure in Frame object 'curr_frame'

    @type curr_measure: Frame
    @rtype: None
    """
    for curr_note in curr_measure.notes:
        if curr_note.index % 8 in [2, 6]:
            curr_note.value = 'snare'
        else:
            curr_note.value = 'rest'


def write_closed_hats(curr_measure):
    """Writes the closed hats for a standard measure in Frame object 'curr_frame'

    @type curr_measure: Measure
    @rtype: None
    """
    hats = [10, 20, 30, 40, 50, 60, 70, 80]  # dummy values

    if random.randint(0, 1) == 0:
        for i in range(0, 8, 2):
            hats[i] = 1
    else:
        for i in range(1, 9, 2):
            hats[i] = 1

    if random.randint(0, 2) == 0:
        hats = [1, 1, 1, 1, 1, 1, 1, 1]

    for i, hat in enumerate(hats):
        if hat == 1:
            curr_measure.notes[i].value = 'closed_hat'
        else:
            curr_measure.notes[i].value = 'rest'


def write_open_hats(curr_measure, curr_loop):
    """Writes the open hats for a standard measure in Frame object 'curr_frame'

    @type curr_measure: Measure
    @type curr_loop: Loop
    @rtype: None
    """
    hats = [10, 20, 30, 40, 50, 60, 70, 80]  # dummy values

    if random.randint(0, 4) < 2:
        hats[random.choice([0, 3, 4, 7])] = 1
    elif random.randint(0, 4) < 2:
        indices = []
        for i, hit in enumerate(curr_loop.rhythm_ref):
            if hit == 1:
                indices.append(i)
        hats[random.choice(indices)] = 1

    for i, hat in enumerate(hats):
        if hat == 1:
            curr_measure.notes[i].value = 'open_hat'
        else:
            curr_measure.notes[i].value = 'rest'
