"""Contains/instantiates the objects of type Chord, Voicing, and Family ~

Note that for Voicing, there is a function which resets the objects ~
This is used in cases when the voicings were altered to cater to exceptional chords ~
e.g. II-7b5 vs II-7, Imaj7 does not used #11, etc ~
"""

from class_chord import *
from class_family import *
from class_voicing import *

# Chord(name, quality, interval)

I = Chord('Imaj', 'major', 0)
IV = Chord('IVmaj', 'major', 5)

# Family(name, chords, depth)

diatonic_major = Family('diatonic major', (I, IV), 0)

V = Chord('V7', 'dominant', 7)

primary_dominant = Family('primary_dominant', (V,), 2)

IImin = Chord('II-', 'minor', 2)
IIImin = Chord('III-', 'minor', 4)
VImin = Chord('VI-', 'minor', 9)

diatonic_minor = Family('diatonic minor', (IImin, IIImin, VImin), 0)

V7ofII = Chord('V7/II', 'dominant', 9)
V7ofIII = Chord('V7/III', 'dominant', 11)
V7ofIV = Chord('V7/IV', 'dominant', 0)
V7ofV = Chord('V7/V', 'dominant', 2)
V7ofVI = Chord('V7/VI', 'dominant', 4)

ma_sec_dom = Family('ma_sec_dom', (V7ofII, V7ofIII, V7ofIV, V7ofV, V7ofVI), 4)

V7ofbVI = Chord('V7/bVI', 'dominant', 3)
V7ofbII = Chord('V7/bII', 'dominant', 8)

mi_sec_dom = Family('mi_sec_dom', (V7ofbVI, V7ofbII), 4)

bII = Chord('bIImaj', 'major', 1)
bIII = Chord('bIIImaj', 'major', 3)
bVI = Chord('bVImaj', 'major', 8)
bVII = Chord('bVIImaj', 'major', 10)

mi_major = Family('mi_major', (bII, bIII, bVI, bVII), 1)

Imin = Chord('I-', 'minor', 0)
IVmin = Chord('IV-', 'minor', 5)
Vmin = Chord('V-', 'minor', 7)

mi_minor = Family('mi_minor', (Imin, IVmin, Vmin), 1)

bVII7 = Chord('bVII7', 'dominant', 10)

mi_dominant = Family('mi_dominant', (bVII7,), 2)

subV7ofI = Chord('subV7/I', 'dominant', 1)
subV7ofII = Chord('subV7/II', 'dominant', 3)
subV7ofIV = Chord('subV7/IV', 'dominant', 6)
subV7ofV = Chord('subV7/V', 'dominant', 8)

ma_sub_dominant = Family('ma_sub_dominant', (subV7ofI, subV7ofII, subV7ofIV, subV7ofV), 4)

subV7ofbII = Chord('subV7/bII', 'dominant', 2)
subV7ofbIII = Chord('subV7/bIII', 'dominant', 4)
subV7ofbVI = Chord('subV7/bVI', 'dominant', 9)

mi_sub_dominant = Family('mi_sub_dominant', (subV7ofI, subV7ofII, subV7ofbIII,
                                             subV7ofIV, subV7ofV, subV7ofbVI, subV7ofbII), 4)

families = (diatonic_major, primary_dominant, diatonic_minor,
            ma_sec_dom, mi_sec_dom, mi_major, mi_minor, mi_dominant, ma_sub_dominant,
            mi_sub_dominant)

notes_flat = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']
notes_sharp = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
qualities = ['major', 'minor', 'dominant']


def set_voicings():
    """Resets all voicings ~

    @rtype: list[list[Voicing]]
    """

    # Voicing(notes, depth rating)

    major_voicings = [Voicing([4, 7], 0),
                      Voicing([2, 4, 7], 1),
                      Voicing([4, 7, 9], 1),
                      Voicing([0, 4, 7, 11], 2),
                      Voicing([4, 6, 7, 11], 3),
                      Voicing([4, 7, 9, 11], 3),
                      Voicing([2, 4, 7, 11], 3),
                      Voicing([4, 6, 7, 9, 11], 4),
                      Voicing([2, 4, 6, 7, 11], 4),
                      Voicing([2, 4, 7, 9, 11], 4)]

    minor_voicings = [Voicing([3, 7], 0),
                      Voicing([0, 3, 7], 1),
                      Voicing([0, 3, 7, 10], 2),
                      Voicing([2, 3, 7, 10], 3),
                      Voicing([3, 5, 7, 10], 3),
                      Voicing([2, 3, 5, 7, 10], 4)]

    dom_voicings = [Voicing([4, 10], 0),
                    Voicing([4, 7, 10], 1),
                    Voicing([0, 4, 7, 10], 2),
                    Voicing([2, 4, 9, 10], 3),
                    Voicing([2, 4, 7, 9, 10], 4)]

    return [major_voicings, minor_voicings, dom_voicings]
