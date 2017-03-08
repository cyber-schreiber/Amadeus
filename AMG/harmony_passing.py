"""Decorates a Loop with passing chords ~ """

from class_loop import *
from harmony_voicing import *
from functions import *
import random


def passing_chords(curr_measure, curr_loop):
    """Decorates a Loop with passing chords ~

    @type curr_measure: Measure
    @type curr_loop: Loop
    @rtype: None
    """

    # shell_harm is the first chord of the measure (currently the only chord of the measure)
    shell_harm = curr_measure.notes[0].value['chord']

    if curr_measure.next is None:  # Adding turn-around
        if random.randint(0, 2) == 0 and curr_loop.attributes['tritone'] >= 2:

            # Choosing between subV7/I, V7, and bII for fourth beat of measure
            if curr_loop.attributes['tritone'] >= 2:
                add_chord = random.choice([subV7ofI, V])
            else:
                add_chord = bII

            add_voicing = get_voicing(add_chord, curr_loop, curr_measure.notes[0].value['voicing'])

            curr_measure.notes[6].value = {'chord': add_chord, 'voicing': add_voicing}
            curr_measure.notes[7].value = {'chord': add_chord, 'voicing': add_voicing}

            if random.randint(0, 1) == 0:
                two_five(curr_loop.key['quality'], V, 4, 6, curr_loop, curr_measure, -5)

    elif shell_harm.quality == 'dominant':  # Adding a relative ii to complete a 2-5
        if random.randint(0, 1) == 0:

            if shell_harm not in ma_sub_dominant.chords + mi_sub_dominant.chords:  # not substitute dominant
                delta = random.choice([-5, -5, -5, 1])
            else:  # shell_harm is substitute dominant
                delta = random.choice([1, 1, 1, -5])

            # first (and currently only) chord of the next measure; curr_measure.next is never None, since the last
            # Measure of Frame.measures is caught by first 'if' statement
            next_shell = curr_measure.next.notes[0].value['chord']

            two_five(next_shell.quality, shell_harm, 0, 4, curr_loop, curr_measure, delta)

    elif random.randint(0, 1) == 0:
        # If (2-4) tritone rating: adding subV7 or V7 (with possible relative ii) to prepare next chord
        # If (0-1) tritone rating: adding chill chords on third and/or fourth beat for variety

        next_shell = curr_measure.next.notes[0].value['chord']

        # Low tritone rating; return None at end of 'if' block
        if curr_loop.attributes['tritone'] < 2:
            chord_options = diatonic_major.chords + diatonic_minor.chords + mi_major.chords + mi_minor.chords

            # This code runs twice such that there may be distinct chords on third and fourth beat
            for _ in range(2):
                add_chord = random.choice(chord_options)
                add_voicing = get_voicing(add_chord, curr_loop, curr_measure.notes[0].value['voicing'])

                # Adding the new chord to either the final half or final quarter of the measure
                for i in range(random.choice([4, 6]), 8):
                    curr_measure.notes[i].value = {'chord': add_chord, 'voicing': add_voicing}

            return

        # Adding a substitute or secondary dominant chord on third or fourth beat (if one resolves properly)
        for add_chord in ma_sub_dominant.chords + mi_sub_dominant.chords + ma_sec_dom.chords + mi_sec_dom.chords:

            if (next_shell.interval in [add_chord.interval + 11, add_chord.interval - 1] and
                add_chord in ma_sub_dominant.chords + mi_sub_dominant.chords) or \
                    (next_shell.interval in [add_chord.interval + 5, add_chord.interval - 7] and
                     add_chord in ma_sec_dom.chords + mi_sec_dom.chords):

                add_voicing = get_voicing(add_chord, curr_loop, curr_measure.notes[0].value['voicing'])
                for i in range(random.choice([4, 6]), 8):
                    curr_measure.notes[i].value = {'chord': add_chord, 'voicing': add_voicing}

                # Adding a relative ii
                if random.randint(0, 2) == 0:
                    two_five(next_shell.quality, add_chord, 4, 6, curr_loop, curr_measure, 1)

                return


def two_five(factor, relative_v, start, stop, curr_loop, curr_measure, delta):
    """Adds a relative ii before a dominant chord. This is a mutating function ~

    @type factor: str
        either 'major', 'minor', or 'dominant'
    @type relative_v: Chord
    @type start: int
    @type stop: int
    @type curr_loop: Loop
    @type curr_measure: Measure
    @type delta: int
        distance between 2 and 5; if 5 is tritone substitute, delta is 1. else, delta is -5.
    @rtype: None
    """

    interval = (relative_v.interval + delta) % 12

    if factor == 'major' or factor == 'dominant':
        add_chord = Chord('relII-', 'minor', interval)
    else:  # factor == 'minor'
        add_chord = Chord('relII-7b5', 'minor', interval)

    add_voicing = get_voicing(add_chord, curr_loop, curr_measure.notes[0].value['voicing'])

    for i in range(start, stop):
        curr_measure.notes[i].value = {'chord': add_chord, 'voicing': add_voicing}
