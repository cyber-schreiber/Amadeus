"""Fills the default/empty Frames of Loop's harm attribute ~

These include 'shell', 'passing', 'rhythm', and 'final' ~
"""

from harmony_shell import *
from harmony_passing import *
from harmony_voicing import *


def construct_harmony(curr_loop):
    """Fills the empty Frames of Loop's (curr_loop) harm attribute ~
    This is a mutating function ~

    @type curr_loop: Loop
    @rtype: None
    """

    # Constructing the shell chords
    prev_chord = None
    prev_voice = None

    for i in range(curr_loop.measures):
        curr_chord = shell_chord(curr_loop, i, prev_chord)
        curr_voice = get_voicing(curr_chord, curr_loop, prev_voice)

        prev_chord = curr_chord
        prev_voice = curr_voice

        for curr_note in curr_loop.harm['shell'].measures[i].notes:
            curr_note.value = {'chord': curr_chord, 'voicing': curr_voice}

    # Decorating with passing chords
    curr_loop.harm['passing'] = curr_loop.harm['shell'].extend().collapse(curr_loop)
    for curr_measure in curr_loop.harm['passing'].measures:
        passing_chords(curr_measure, curr_loop)

    # Constructing the rhythmic attack/sustain Frame
    temp_harm = curr_loop.harm['rhythm'].extend()
    for curr_note in temp_harm.measures[0].notes:
        if curr_note.index == 0:
            curr_note.value = 'A'
        elif curr_loop.harm['passing'][curr_note.index].value == curr_loop.harm['passing'][curr_note.index-1].value:
            curr_note.value = 'S'
        else:
            curr_note.value = 'A'
    curr_loop.harm['rhythm'] = temp_harm.collapse(curr_loop)

    # Constructing the final compressed harmony Frame
    curr_loop.harm['final'] = curr_loop.harm['passing'].extend().collapse(curr_loop)
    curr_loop.harm['final'].compress()
