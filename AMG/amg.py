"""
This contains code for the Automatic Music Generator
"""

import random


class Family:
    """Represents a chord family which has a name and tension/depth ratings.

    @type name: str
    @type chords: (Chord, Chord, ...)
    @type tension: int
    @type depth: int
    @type weight: int
    """

    def __init__(self, name, chords, tension, depth):
        """Constructs a chord family

        @type self: Family
        @type name: str
        @type chords: (Chord, Chord, ...)
        @type tension: int
        @type depth: int
        @rtype: None
        """

        self.name = name
        self.chords = chords
        self.tension = tension
        self.depth = depth
        self.weight = 0

    def determine_weight(self, loop):
        """Determines the weight of family self based on loop settings, and
        mutates self's attribute accordingly

        @type self: Family
        @type loop: Loop
        @rtype: None
        """

        self.weight = int(10 - ((self.tension - loop.tension) ** 2 * 2.5))

        # accounting for diatonic chords keeping in play
        if self.name == 'primary_dominant' or self.name == 'diatonic major' or \
                self.name == 'diatonic minor':
            if loop.tension > 2:
                self.weight = 2
        elif self.name == 'mi_dominant' or self.name == 'primary_dominant':
            if loop.tension < 2:
                self.weight = 0
            elif loop.tension > 2:
                self.weight -= 4


class Loop:
    """Represents a loop which has one or more keys, a number of measures,
    a tension rating, and a depth rating.

    @type key: (str, str)
        the key e.g. ('Bb', 'major')
    @type measures: int
    @type tension: int
    @type depth: int
    @type chords: list[int]
        the chords belonging to this loop

    Representation Invariants:
    len(keys) >= 1
    int objects in keys add up to measures
    0 <= tension <= 4
    0 <= depth <= 4
    """

    def __init__(self, measures, tension, depth):
        """Constructs a new loop

        @type self: Loop
        @type measures: int
        @type tension: int
        @type depth: int
        @rtype: None
        """

        self.key = (notes[random.randint(0, 11)], qualities[0])
        # qualities[0] means it is major (sufficient for now)
        self.measures = measures
        self.tension = tension
        self.depth = depth
        self.chords = []


class Chord:
    """Represents a chord which has a family, level of tension,
    and level of depth.

    @type family: str
    @type name: str
    @type quality: str
        either major, minor, or dominant
    @type tension: int
        0 is most relaxed, 4 is most tense
    @type depth: int
        0 is most shallow, 4 is most deep
    @type quality: str
        the quality of the chord
    @type interval: int
        the distance (in semi-tones) between this chord's root and the tonic
    @type chord_scale: list[int]
        the notes which are available to play over this chord

    0 <= tension <= 4
    0 <= depth <= 4
    """

    def __init__(self, family, name, quality, tension, depth, interval):
        """Constructs a chord

        @type self: Chord
        @type family: str
        @type name: str
        @type quality: str
        @type tension: int
        @type depth: int
        @type interval: int
        @rtype: None
        """

        self.family = family
        self.name = name
        self.quality = quality
        self.tension = tension
        self.depth = depth
        self.interval = interval

        if quality == 'major':
            self.chord_scale = [2, 4, 6, 7, 9, 11]
            if name == 'Imaj':
                self.chord_scale.remove(6)
        elif quality == 'minor':
            self.chord_scale = [0, 2, 3, 5, 7, 10]
            if name == 'III-':
                self.chord_scale.remove(2)
        elif name == 'V7' or name == 'bVII7' or name == 'V7/IV' or \
                name == 'V7/V':
            self.chord_scale = [0, 2, 4, 7, 9, 10]
        elif name == 'V7/II':
            self.chord_scale = [0, 2, 4, 7, 8, 10]
        elif name == 'V7/III' or name == 'V7/VI':
            self.chord_scale = [0, 1, 3, 4, 7, 8, 10]

        self.weight = 0


class Voicing:
    """Represents the particular notes of a four-voice chord

    @type quality: str
    @type notes: list[int]
    @type depth: int
    """

    def __init__(self, quality, notes, depth):
        """Constructs a voicing

        @type self: Voicing
        @type quality: str
        @type notes: list[int]
        @type depth: int
        @rtype: None
        """

        self.quality = quality
        self.notes = notes
        self.depth = depth


def choose_chord(current_loop, measure, previous_chord):
    """Determines the next chord for the loop.

    @type current_loop: Loop
    @type measure: int
    @type previous_chord: Chord
    @rtype: Chord
    """
    if previous_chord is None or measure == 0 or \
            previous_chord.name == 'bVIImaj' or previous_chord.name == 'bVII7':
        return diatonic_major.chords[0]

    elif previous_chord.name == 'V7':
        return_lst = [I, I, I, I, VImin]
        if current_loop.tension > 2 and measure != current_loop.measures - 1:
            return_lst.extend([V7ofIV, V7ofIV, V7ofIV])
        return random.choice(return_lst)

    elif current_loop.tension > 2 and measure == current_loop.measures - 1 and \
            previous_chord.quality != 'dominant':
        return V

    elif previous_chord.quality == 'dominant':  # dominant resolution
        e = True
        while e:
            chord_family = choose_family(current_loop)
            return_chords = []
            return_chord = None
            for chord_change in chord_family.chords:
                if previous_chord.interval - chord_change.interval == 7 or \
                        previous_chord.interval - chord_change.interval == -5:
                    e = False
                    return_chords.append(chord_change)
                    return_chords.append(chord_change)
                    return_chords.append(chord_change)
                if (previous_chord.interval - chord_change.interval == 10 or
                        previous_chord.interval - chord_change.interval == -2) \
                        and chord_change.quality == 'minor':
                    return_chords.append(chord_change)
                    e = False

            if len(return_chords) > 0:
                return_chord = random.choice(return_chords)

            if measure == current_loop.measures - 1 and \
                    return_chord is not None:
                if return_chord.quality == 'dominant' and \
                                return_chord.name != 'V7':
                    e = True

        return return_chord

    elif measure == current_loop.measures - 1:
        # final chord should not be dominant (except primary dominant)
        true = True
        while true:
            chord_family = choose_family(current_loop)
            if chord_family.chords[0].quality != 'dominant' and \
               chord_family.chords[0].name != 'V7':
                true = False
        return get_chord(chord_family, previous_chord)

    else:
        chord_family = choose_family(current_loop)
        return get_chord(chord_family, previous_chord)


def get_chord(family, previous_chord):
    """Determines which chord from the family will be played based on the
    interval from the previous chord

    @type family: Family
    @type previous_chord: Chord
    @rtype: Chord
    """
    chord_selection = []

    for chord in family.chords:
        interval = abs(chord.interval - previous_chord.interval)
        if interval > 6:
            interval = 12 - interval
        if interval == 0:
            chord_selection.append(chord)
        elif interval == 1:
            chord_selection.append(chord)
            chord_selection.append(chord)
            chord_selection.append(chord)
            chord_selection.append(chord)
        elif interval == 2:
            chord_selection.append(chord)
            chord_selection.append(chord)
        elif interval == 3:
            chord_selection.append(chord)
            chord_selection.append(chord)
            chord_selection.append(chord)
        elif interval == 4:
            chord_selection.append(chord)
            chord_selection.append(chord)
            chord_selection.append(chord)
        elif interval == 5:
            chord_selection.append(chord)
            chord_selection.append(chord)
            chord_selection.append(chord)
            chord_selection.append(chord)
        elif interval == 6:
            chord_selection.append(chord)
            chord_selection.append(chord)

    return random.choice(chord_selection)


def choose_family(loop):
    """Determines which chord family the next chord will belong to
    based on chillness and depth ratings

    @type loop: Loop
    @rtype: Family
    """
    choice_generator = []

    for familia in families:
        familia.determine_weight(loop)
        for _ in range(familia.weight):
            choice_generator.append(families.index(familia))

    choice = families[random.choice(choice_generator)]
    return choice


def get_chord_name(chord_device, loop):
    """Returns the name of the chord chord_device according to its relation
    to the tonic.

    Used when printing functional chord symbol and relating it to a key.

    @type chord_device: Chord
    @type loop: Loop
    @rtype: str
    """
    tonic = loop.key[0]
    interval = notes.index(tonic) + chord_device.interval
    if interval < 12:
        root = notes[interval]
    else:
        interval -= 12
        root = notes[interval]
    quality = chord_device.quality
    if quality == 'dominant':
        quality = '7'
    elif quality == 'major':
        quality = 'maj '
    else:  # quality == 'minor
        quality = '-'
    name = root + quality
    while len(name) < 6:
        name += ' '
    return name


def get_voicing(chord, loop, prev_voice, measure_counter):
    """Calculates and returns a voicing for a chord based on loop's properties

    @type chord: Chord
    @type loop: Loop
    @type prev_voice: str
    @type measure_counter: int
    @rtype: str 'A B C D'
    """
    if chord.quality == 'major':
        voicing_options = voicings[0]
    elif chord.quality == 'minor':
        voicing_options = voicings[1]
    else:  # chord.quality == 'dominant'
        if chord.name == 'V7/IV' or chord.name == 'V7/V' or \
                chord.name == 'bVII7' or chord.name == 'V7':
            voicing_options = voicings[2]
        elif chord.name == 'V7/II':
            voicing_options = voicings[3]
        else:  # chord.name == 'V7/III' or chord.name == 'V7/VI'
            voicing_options = voicings[4]

    candidates = []
    for voice in voicing_options:
        if voice.depth == loop.depth:
            candidates.append(voice)

    voice = random.choice(candidates)

    str_to_return = ''

    root_value = notes.index(loop.key[0]) + chord.interval
    if root_value > 11:
        root_value -= 12

    for note in voice.notes:
        new_note = root_value + note
        if new_note > 11:
            new_note -= 12
        str_to_return += notes[new_note] + ' '

    if measure_counter != 0:
        if loop.depth == 0:
            str_to_return = get_inversion(str_to_return, prev_voice, 2)
        elif loop.depth == 1:
            str_to_return = get_inversion(str_to_return, prev_voice, 3)
        elif 2 <= loop.depth <= 3:
            str_to_return = get_inversion(str_to_return, prev_voice, 4)
        else:  # loop.depth == 4
            str_to_return = get_inversion(str_to_return, prev_voice, 5)

    return str_to_return


def get_inversion(two_notes, prev_voice, number_of_voices):
    """Calculates and returns the inversion optional for two-note voice-leading

    @type two_notes: str 'A B'
    @type prev_voice: str
    @type number_of_voices: int
        0 <= number_of_voices <= 4
    @rtype: str 'A B'
    """
    distances = []
    for _ in range(number_of_voices):
        distances.append(0)
    characters = []
    char1 = ''
    for char in two_notes:
        if char != ' ':
            char1 += char
        else:
            characters.append(char1)
            char1 = ''

    if number_of_voices == 2:
        note_sets = [characters, characters[1:] + characters[:1]]
    elif number_of_voices == 3:
        note_sets = [characters, characters[1:] + characters[:1],
                     characters[2:] + characters[:2]]
    elif number_of_voices == 4:
        note_sets = [characters, characters[1:] + characters[:1],
                     characters[2:] + characters[:2],
                     characters[3:] + characters[:3]]
    else:  # number_of_voices == 5
        note_sets = [characters, characters[1:] + characters[:1],
                     characters[2:] + characters[:2],
                     characters[3:] + characters[:3],
                     characters[4:] + characters[:4]]

    # Ensuring there will not be semi-tones at the top of a voice-lead
    if number_of_voices > 3:
        for note_set in note_sets:
            if abs(notes.index(note_set[2]) - notes.index(note_set[3])) == 1 \
                    or abs(notes.index(note_set[0]) - notes.index(
                                note_set[1])) == 1:
                distances[note_sets.index(note_set)] += 100

    prev_characters = []
    char2 = ''

    for char in prev_voice:
        if char != ' ':
            char2 += char
        else:
            prev_characters.append(char2)
            char2 = ''

    for note_set in note_sets:
        for i in range(number_of_voices):
            first = note_set[i]
            second = prev_characters[i]
            interval = abs(notes.index(first)-notes.index(second))
            if interval > 6:
                interval = 12 - interval
            distances[note_sets.index(note_set)] += interval

    minimum = distances.index(min(distances))
    char3 = ''
    for char in note_sets[minimum]:
        char3 += char + ' '
    return char3


# (family, name, quality, mellow/dry, depth, interval)

I = Chord('diatonic major', 'Imaj', 'major', 0, 0, 0)
IV = Chord('diatonic major', 'IVmaj', 'major', 0, 0, 5)

diatonic_major = Family('diatonic major', (I, IV), 0, 0)

V = Chord('diatonic major', 'V7', 'dominant', 2, 1, 7)

primary_dominant = Family('primary_dominant', (V,), 2, 1)

IImin = Chord('diatonic minor', 'II-', 'minor', 0, 0, 2)
IIImin = Chord('diatonic minor', 'III-', 'minor', 0, 0, 4)
VImin = Chord('diatonic minor', 'VI-', 'minor', 0, 0, 9)

diatonic_minor = Family('diatonic minor', (IImin, IIImin, VImin), 0, 0)

V7ofII = Chord('secondary dominant', 'V7/II', 'dominant', 4, 2, 9)
V7ofIII = Chord('secondary dominant', 'V7/III', 'dominant', 4, 2, 11)
V7ofIV = Chord('secondary dominant', 'V7/IV', 'dominant', 4, 2, 0)
V7ofV = Chord('secondary dominant', 'V7/V', 'dominant', 4, 2, 2)
V7ofVI = Chord('secondary dominant', 'V7/VI', 'dominant', 4, 2, 4)

sec_dom = Family('sec_dom', (V7ofII, V7ofIII, V7ofIV, V7ofV, V7ofVI), 4, 2)

bII = Chord('modal interchange major', 'bIImaj', 'major', 1, 3, 1)
bIII = Chord('modal interchange major', 'bIIImaj', 'major', 1, 3, 3)
bVI = Chord('modal interchange major', 'bVImaj', 'major', 1, 3, 8)
bVII = Chord('modal interchange major', 'bVIImaj', 'major', 1, 3, 10)

mi_major = Family('mi_major', (bII, bIII, bVI, bVII), 1, 3)

Imin = Chord('modal interchange minor', 'I-', 'minor', 1, 3, 0)
IVmin = Chord('modal interchange minor', 'IV-', 'minor', 1, 3, 5)
Vmin = Chord('modal interchange minor', 'V-', 'minor', 1, 3, 7)

mi_minor = Family('mi_minor', (IVmin, Vmin), 1, 3)

bVII7 = Chord('modal interchange dominant', 'bVII7', 'dominant', 2, 2, 10)

mi_dominant = Family('mi_dominant', (bVII7,), 2, 3)

families = (diatonic_major, primary_dominant, diatonic_minor,
            sec_dom, mi_major, mi_minor, mi_dominant)

notes = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab']
qualities = ['major', 'minor', 'dominant']

major_voicings = [Voicing('major', [4, 7], 0),
                  Voicing('major', [2, 4, 7], 1),
                  Voicing('major', [4, 7, 9], 1),
                  Voicing('major', [0, 4, 7, 11], 2),
                  Voicing('major', [4, 6, 7, 11], 3),
                  Voicing('major', [4, 7, 9, 11], 3),
                  Voicing('major', [2, 4, 7, 11], 3),
                  Voicing('major', [4, 6, 7, 9, 11], 4),
                  Voicing('major', [2, 4, 6, 7, 11], 4),
                  Voicing('major', [2, 4, 7, 9, 11], 4)]

minor_voicings = [Voicing('minor', [3, 7], 0),
                  Voicing('minor', [2, 3, 7], 1),
                  Voicing('minor', [3, 5, 7], 1),
                  Voicing('minor', [0, 3, 7, 10], 2),
                  Voicing('minor', [2, 3, 7, 10], 3),
                  Voicing('minor', [3, 5, 7, 10], 3),
                  Voicing('minor', [2, 3, 5, 7, 10], 4)]

dom_voicings = [Voicing('dominant natural', [4, 10], 0),
                Voicing('dominant natural', [4, 7, 10], 1),
                Voicing('dominant natural', [0, 4, 7, 10], 2),
                Voicing('dominant natural', [2, 4, 9, 10], 3),
                Voicing('dominant natural', [2, 4, 7, 9, 10], 4)]

dom_voicings_b13 = [Voicing('dominant b13', [4, 10], 0),
                    Voicing('dominant b13', [4, 8, 10], 1),
                    Voicing('dominant b13', [0, 4, 7, 10], 2),
                    Voicing('dominant b13', [2, 4, 8, 10], 3),
                    Voicing('dominant b13', [2, 4, 6, 8, 10], 4)]

dom_voicings_b9_b13 = [Voicing('dominant b9 b13', [4, 10], 0),
                       Voicing('dominant b9 b13', [4, 8, 10], 1),
                       Voicing('dominant b9 b13', [0, 4, 7, 10], 2),
                       Voicing('dominant b9 b13', [1, 4, 8, 10], 3),
                       Voicing('dominant b9 b13', [1, 4, 6, 8, 10], 4)]

voicings = [major_voicings, minor_voicings, dom_voicings, dom_voicings_b13,
            dom_voicings_b9_b13]


if __name__ == "__main__":

    a = True
    while a:
        b = True
        while b:
            measures_input = input("How many measures is your loop? "
                                   "(2, 4, 8, 16) ")
            if measures_input == '2' or measures_input == '4' or\
               measures_input == '8' or measures_input == '16':
                measures_input = int(measures_input)
                b = False

        c = True
        while c:
            tension_input = input("How mellow is your loop? "
                                  "(very mellow, mellow, in between, "
                                  "dry, very dry) ")
            if tension_input == 'very mellow':
                tension_input = 0
                c = False
            elif tension_input == 'mellow':
                tension_input = 1
                c = False
            elif tension_input == 'in between':
                tension_input = 2
                c = False
            elif tension_input == 'dry':
                tension_input = 3
                c = False
            elif tension_input == 'very dry':
                tension_input = 4
                c = False

        d = True
        while d:
            depth_input = input("How deep is your loop? (very shallow, "
                                "shallow, in between, deep, very deep) ")

            if depth_input == 'very shallow':
                depth_input = 0
                d = False
            elif depth_input == 'shallow':
                depth_input = 1
                d = False
            elif depth_input == 'in between':
                depth_input = 2
                d = False
            elif depth_input == 'deep':
                depth_input = 3
                d = False
            elif depth_input == 'very deep':
                depth_input = 4
                d = False

        loop = Loop(measures_input, tension_input, depth_input)

        print()

        for measure_counter in range(loop.measures):
            if measure_counter == 0:
                previous = None
                previous_voice = None

            chord = choose_chord(loop, measure_counter, previous)
            previous = chord

            voice = get_voicing(chord, loop, previous_voice, measure_counter)
            previous_voice = voice

            print(get_chord_name(chord, loop),
                  chord.name, ' '*(7-len(chord.name)),
                  voice)

        print()
        again = input('again? (y/n) ')
        print()
        if again == 'n':
            a = False
