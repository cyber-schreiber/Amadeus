"""Fills the default/empty Frames of Loop's harm attribute ~

These include 'kick', 'snare', 'closed_hat', and 'open_hat' ~
"""

from perc_write import *


def construct_percussion(curr_loop):
    """Fills the Frames for percussion in a Loop (curr_loop)

    @type curr_loop: Loop
    @rtype: None
    """

    # Fill kick Frame
    for i, curr_measure in enumerate(curr_loop.perc['kick'].measures):
        if i == 0 or i == curr_loop.measures-1 or (i+1) == (curr_loop.measures/2) and random.randint(0, 1) == 0:
            write_kicks(curr_measure, curr_loop)
        else:
            for i2, curr_note in enumerate(curr_loop.perc['kick'].measures[0].notes):
                curr_measure.notes[i2].value = curr_note.value

    # Fill snare Frame
    for i, curr_measure in enumerate(curr_loop.perc['snare'].measures):
        if i == 0 or i == curr_loop.measures - 1 or (i+1) == (curr_loop.measures/2) and random.randint(0, 1) == 0:
            write_snares(curr_measure)
        else:
            for i2, curr_note in enumerate(curr_loop.perc['snare'].measures[0].notes):
                curr_measure.notes[i2].value = curr_note.value

    # Fill closed_hat Frame
    for i, curr_measure in enumerate(curr_loop.perc['closed_hat'].measures):
        if i == 0 or i == curr_loop.measures - 1 or (i+1) == (curr_loop.measures/2) and random.randint(0, 1) == 0:
            write_closed_hats(curr_measure)
        else:
            for i2, curr_note in enumerate(curr_loop.perc['closed_hat'].measures[0].notes):
                curr_measure.notes[i2].value = curr_note.value

    # Fill open_hat Frame
    for i, curr_measure in enumerate(curr_loop.perc['open_hat'].measures):
        if i == 0 or i == curr_loop.measures - 1 or (i + 1) == (curr_loop.measures / 2) and random.randint(0, 1) == 0:
            write_open_hats(curr_measure, curr_loop)
        else:
            for i2, curr_note in enumerate(curr_loop.perc['open_hat'].measures[0].notes):
                curr_measure.notes[i2].value = curr_note.value
