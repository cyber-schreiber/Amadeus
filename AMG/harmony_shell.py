"""Writes the block chords for a loop"""

from class_loop import *
from functions import *
import random


def shell_chord(curr_loop, curr_measure, prev_chord):
    """Determines the next shell chord for the loop ~

    First checks for exceptional case ~
        i) first chord of measure -> return I/I-
        ii) prev chord was bVIImaj or bVII7 -> return I/I-
        iii) final chord of measure & (3-4) tritone rating -> if there is no dominant resolution conflict, return V7
        iv) prev chord was dominant -> return chord down a fifth OR up a second OR down a semi-tone
        v) final chord of measure & (0-2) tritone rating -> ensure final chord is not dominant not resolving to I/I-

    If case is not exceptional, finds a family based on tritone rating ~
    and from family selects a chord based on interval ~

    @type curr_loop: Loop
    @type curr_measure: int
    @type prev_chord: Chord | None
    @rtype: Chord
    """

    # To resolve bVII chords, and for the first chord in the loop: return I or I-
    if curr_measure == 0 or prev_chord.name in ['bVIImaj', 'bVII7']:
        if curr_loop.key['quality'] == 'major':
            return I
        else:  # curr_loop.key['quality'] == 'minor'
            return Imin

    # (3-4) tritone rating of curr_loop AND final chord of loop: return V
    elif curr_loop.attributes['tritone'] > 2 and curr_measure == curr_loop.measures - 1 and \
            (prev_chord.quality != 'dominant' or prev_chord.name == 'V7/V' or prev_chord.name == 'subV7/V'):
        return V

    # Dominant resolution
    elif prev_chord.quality == 'dominant':
        return dominant_resolution(curr_loop, curr_measure, prev_chord)

    # Final chord should not be dominant (except primary dominant)
    elif curr_measure == curr_loop.measures - 1:
        true = True
        while true:
            chord_family = choose_family(curr_loop)
            if chord_family.chords[0].quality != 'dominant' or \
                    chord_family.chords[0].quality == 'dominant' and chord_family.chords[0].name == 'V7':
                true = False
        return choose_chord(chord_family, prev_chord)

    # Not an exceptional case; default chord selection procedure
    else:
        return choose_chord(choose_family(curr_loop), prev_chord)


def dominant_resolution(curr_loop, curr_measure, prev_chord):
    """Finds an appropriate chord to follow a dominant 7th chord

    @type curr_loop: Loop
    @type curr_measure: int
    @type prev_chord: Chord | None
    @rtype: Chord
    """

    # case I: V7/bII goes to bII, V or subV7ofI (V7/bII is rare case)
    if prev_chord.name == 'V7ofbII':
        return_lst = [V, V, subV7ofI]
        if curr_loop.attributes['tension'] < 3:
            return_lst.extend([bII, bII, bII])
        return random.choice(return_lst)

    # case II: return either a chord 7 semitones below (equivalent to 5 above), 2 up / 10 down, or 1 down / 11 up
    e = True
    while e:
        chord_family = choose_family(curr_loop)
        return_chords = []
        return_chord = None

        for chord_change in chord_family.chords:

            # Resolve down perfect 5th (7 semi-tones)
            if (prev_chord.interval - chord_change.interval) % 12 == 7:
                e = False
                return_chords.append(chord_change)
                if prev_chord.name[:5] != 'subV7':
                    return_chords.extend([chord_change, chord_change, chord_change])

            # Resolve up major 2nd (2 semi-tones)
            if (prev_chord.interval - chord_change.interval) % 12 == 10:
                return_chords.append(chord_change)

            # Resolve down minor 2nd (1 semi-tone)
            if (prev_chord.interval - chord_change.interval) % 12 == 1:
                e = False
                return_chords.append(chord_change)
                if prev_chord.name[:5] == 'subV7':
                    return_chords.extend([chord_change, chord_change, chord_change])

        # If chords from the chosen family have been found to be appropriate intervals from the previous chord
        # for dominant resolution, assign return_chord to a random choice of those chords
        if len(return_chords) > 0:
            return_chord = random.choice(return_chords)

        # For final chord of measure, if a dominant chord that does not resolve to tonic has been selected
        # then run the while loop again to find a new chord
        if curr_measure == curr_loop.measures - 1 and return_chord is not None:
            if return_chord.quality == 'dominant' and return_chord.name != 'V7':
                e = True

    return return_chord


def choose_family(curr_loop):
    """Determines which chord family the next chord will belong to based on tritone ratings ~
    Used by block_chord() ~

    Higher tritone rating implies that a dominant chord family will be chosen ~
    Lower tritone rating implies that a major/minor chord family will be chosen ~

    @type curr_loop: Loop
    @rtype: Family
    """
    return_families = []

    for curr_family in families:
        curr_family.determine_weight(curr_loop)

        for _ in range(curr_family.weight):
            return_families.append(families.index(curr_family))

    return families[random.choice(return_families)]


def choose_chord(curr_family, prev_chord):
    """Determines which chord from the family will be played based on the interval from the previous chord ~
    Used by block_chord() ~

    Higher 'add_val' values mean the chord is more acceptable to the ear ~
    This is a *subjective* judgment, and may be improved ~

    @type curr_family: Family
    @type prev_chord: Chord
    @rtype: Chord
    """
    return_chords = []

    for chord in curr_family.chords:
        interval = abs(chord.interval - prev_chord.interval)
        if interval > 6:
            interval = 12 - interval
        if interval == 0:
            add_val = 1
        elif interval == 1:
            add_val = 4
        elif interval == 2:
            add_val = 2
        elif interval == 3:
            add_val = 3
        elif interval == 4:
            add_val = 3
        elif interval == 5:
            add_val = 4
        else:  # interval == 6
            add_val = 1

        for _ in range(add_val):
            return_chords.append(chord)

    return random.choice(return_chords)
