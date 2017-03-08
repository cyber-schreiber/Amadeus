"""This contains miscellaneous functions which are not particular to an Amadeus-defined class ~

They are used for reference ~
"""

from harmony_objects import *


def get_enharmonic(curr_note):
    """Returns an enharmonic spelling of a black key

    @type curr_note: str
        e.g. 'Ab' or 'C#'
    @rtype: str
        e.g. 'G#' or 'Db'
    """
    if curr_note == 'Ab':
        return 'G#'
    if curr_note == 'Bb':
        return 'A#'
    if curr_note == 'Db':
        return 'C#'
    if curr_note == 'Eb':
        return 'D#'
    if curr_note == 'Gb':
        return 'F#'
    if curr_note == 'A#':
        return 'Bb'
    if curr_note == 'C#':
        return 'Db'
    if curr_note == 'D#':
        return 'Eb'
    if curr_note == 'F#':
        return 'Gb'
    if curr_note == 'G#':
        return 'Ab'


def key_sharp_or_flat(curr_key):
    """Takes a key and returns whether it has sharps or flats

    @type curr_key: (str, str)
        e.g. ('A', 'major')
    @rtype: str
        either 's' for sharp or 'f' for flat
    """

    if curr_key['quality'] == 'major':
        if curr_key['root'] in ['C', 'D', 'E', 'G', 'A', 'B', 'C#', 'D#', 'F#', 'G#', 'A#']:
            return notes_sharp
        else:  # curr_key['root'] in notes not listed above (including enharmonic spellings)
            return notes_flat
    else:  # curr_key['quality'] == 'minor'
        if curr_key['root'] in ['E', 'B', 'F#', 'C#', 'G#', 'D#', 'A#']:
            return notes_sharp
        else:  # curr_key['root'] not in notes listed above (including enharmonic spellings)
            return notes_flat


def diatonic(curr_chord, curr_loop):
    """Returns whether the chord is diatonic to the loop ~

    @type curr_chord: Chord
    @type curr_loop: Loop
    @rtype: bool
    """

    if curr_loop.key['quality'] == 'major':
        diatonic_families = [diatonic_major, diatonic_minor, primary_dominant, ma_sec_dom]
    else:  # curr_loop.key[0] == 'minor'
        diatonic_families = [mi_major, mi_minor, mi_dominant, mi_sec_dom]

    diatonic_chords = []
    for temp_family in diatonic_families:
        for temp_chord in temp_family.chords:
            diatonic_chords.append(temp_chord)

    if curr_chord in diatonic_chords:
        return True
    else:
        return False


def chord_sharp_or_flat(curr_chord, curr_loop):
    """Takes a chord in a loop and returns whether it should be labelled with notes that are sharp or flat ~

    @type curr_chord: Chord
    @type curr_loop: Loop
    @rtype: lst
        either sharp_notes or flat_notes
    """

    # i) determine whether loop.key uses sharps or flats
    # ii) determine whether chord is diatonic -> if so, return whether loop.key uses sharps or flats. if not ->
    # iii) if not, determine whether the key of the chord scale is sharp or flat

    if diatonic(curr_chord, curr_loop):
        return key_sharp_or_flat(curr_loop.key)
    else:
        if curr_chord.quality == 'dominant':
            quality = 'major'
        else:
            quality = curr_chord.quality
        if get_chord_name(curr_chord, curr_loop)[1] == 'b' or get_chord_name(curr_chord, curr_loop)[1] == '#':
            root = get_chord_name(curr_chord, curr_loop)[:2]
        else:
            root = get_chord_name(curr_chord, curr_loop)[0]
        return key_sharp_or_flat({'root': root, 'quality': quality})


def get_chord_name(curr_chord, curr_loop):
    """Returns the name of the chord according to its relation to the tonic ~

    Used when printing functional chord symbol and relating it to a key ~

    @type curr_chord: Chord
    @type curr_loop: Loop
    @rtype: str
    """
    key_sorf = key_sharp_or_flat(curr_loop.key)
    tonic = curr_loop.key['root']

    if key_sorf == notes_sharp:
        interval = (notes_sharp.index(tonic) + curr_chord.interval) % 12
    else:  # sharp_or_flat == notes_flat
        interval = (notes_flat.index(tonic) + curr_chord.interval) % 12

    if diatonic(curr_chord, curr_loop):
        # Chord is diatonic; # or b will be the same as the key
        root = key_sharp_or_flat(curr_loop.key)[interval]

    else:
        # Chord is not diatonic; if key is major, Chord is b; if minor, Chord is #; this pattern may not be 100%
        # precise or complete, however it is applicable to the vast majority of cases
        if curr_loop.key['quality'] == 'major':
            root = notes_flat[interval]
        else:
            root = notes_sharp[interval]

    quality = curr_chord.quality
    if quality == 'dominant':
        quality = '7'
    elif quality == 'major':
        quality = 'maj'
    else:  # quality == 'minor'
        quality = '-'

    if curr_chord.name in ['relII-7b5', 'II-7b5']:
        quality += '7b5'

    name = root + quality

    return name
