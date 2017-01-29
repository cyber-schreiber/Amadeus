"""
This contains code for the Automatic Music Generator
"""

import random


class Family:
    """Represents a chord family which has a name and tension/depth ratings.

    @type name: str
    @type chords: (Chord, Chord, ...)
    @type dry: int
    @type weight: int
    """

    def __init__(self, name, chords, dry):
        """Constructs a chord family

        @type self: Family
        @type name: str
        @type chords: (Chord, Chord, ...)
        @type dry: int
        @rtype: None
        """

        self.name = name
        self.chords = chords
        self.dry = dry
        self.weight = 0

    def determine_weight(self, loop):
        """Determines the weight of family self based on loop settings, and
        mutates self's attribute accordingly

        @type self: Family
        @type loop: Loop
        @rtype: None
        """

        self.weight = int(15 - ((self.dry - loop.tension) ** 2 * 2.5))

        # accounting for diatonic chords keeping in play
        if loop.key[1] == 'major':
            if self.name == 'primary_dominant' or self.name == 'diatonic major' or \
                    self.name == 'diatonic minor':
                if loop.tension > 2:
                    self.weight = 2
            if self.name == 'mi_dominant' or self.name == 'primary_dominant':
                if loop.tension < 2:
                    self.weight = 0
                elif loop.tension > 2:
                    self.weight = 2
            if self.name == 'mi_sec_dom':
                self.weight = 1
        else:  # loop.key[1] == 'minor'
            if self.name == 'mi_minor' or self.name == 'mi_major':
                self.weight = 2
            if self.name == 'diatonic major' or self.name == 'diatonic minor' or self.name == 'ma_sec_dom':
                self.weight = 1


class Loop:
    """Represents a loop which has a key, a number of measures,
    a tension rating, and a depth rating.

    @type key: (str, str)
        the key e.g. ('Bb', 'major')
    @type measures: int
    @type tension: int
    @type depth: int
    @type spots: list[Spot]
        the chords belonging to this loop

    Representation Invariants:
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
        onward = False
        while not onward:
            if random.randint(0, 1) == 0:  # flat key
                temp_key = notes_flat[random.randint(0, 11)], 'major'
                if temp_key[0] != 'Gb':
                    onward = True
            else:  # sharp key
                temp_key = notes_sharp[random.randint(0, 11)], 'minor'
                if temp_key[0] != 'A#' and temp_key[0] != 'D#':
                    onward = True

        self.key = temp_key
        self.measures = measures
        self.tension = tension
        self.depth = depth


class Frame:
    """Contains all the rhythmic/timing information of harmony/melody/bass
    of a Loop

    ===Attributes===
    @type melody: list[list[int]]
        len(melody) = number of measures in the loop
    @type bass: list[list[int]]
        len(bass) = len(melody)
    @type harmony: list[list[Chord]]
        len(harmony) = len(bass) = len(melody)
    """

    def __init__(self):
        """Constructs a new frame; this is called when a new loop is creates

        @type self: Frame
        @rtype: None
        """
        self.melody = []
        self.bass = []
        self.harmony = []


class Chord:
    """Represents a chord

    @type name: str
    @type quality: str
        either major, minor, or dominant
    @type quality: str
        the quality of the chord
    @type interval: int
        the distance (in semi-tones) between this chord's root and the tonic
    @type chord_scale: list[int]
        the notes which are available to play over this chord
    """

    def __init__(self, name, quality, interval):
        """Constructs a chord

        @type self: Chord
        @type name: str
        @type quality: str
        @type interval: int
        @rtype: None
        """

        self.name = name
        self.quality = quality
        self.interval = interval

        if quality == 'major':
            self.chord_scale = [2, 4, 6, 7, 9, 11]
            if name == 'Imaj':
                self.chord_scale.remove(6)
        elif quality == 'minor':
            self.chord_scale = [0, 2, 3, 5, 7, 10]
            if name == 'III-':
                self.chord_scale.remove(2)
        else:  # quality == 'dominant'
            if name == 'V7/II':
                self.chord_scale = [0, 2, 4, 7, 8, 10]
            elif name == 'V7/III' or name == 'V7/VI':
                self.chord_scale = [0, 1, 3, 4, 7, 8, 10]
            else:
                self.chord_scale = [0, 2, 4, 7, 9, 10]

        self.weight = 0


class Voicing:
    """Represents the particular notes of a four-voice chord

    @type notes: list[int]
    @type depth: int
    """

    def __init__(self, notes, depth):
        """Constructs a voicing

        @type self: Voicing
        @type notes: list[int]
        @type depth: int
        @rtype: None
        """

        self.notes = notes
        self.depth = depth


def diatonic(curr_chord, curr_loop):
    """Returns whether the chord is diatonic to the loop

    @type curr_chord: Chord
    @type curr_loop: Loop
    @rtype: bool
    """

    if curr_loop.key[1] == 'major':
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
        either 's' or 'f'
    """

    if curr_key[1] == 'major':
        if curr_key[0] in ['C', 'D', 'E', 'G', 'A', 'B', 'C#', 'D#', 'F#', 'G#', 'A#']:
            return 's'
        else:  # curr_key[0] in notes not listed above (including enharmonic spellings)
            return 'f'
    else:  # curr_key[1] == 'minor'
        if curr_key[0] in ['E', 'B', 'F#', 'C#', 'G#', 'D#', 'A#']:
            return 's'
        else:  # curr_key[0] in notes not listed above (including enharmonic spellings)
            return 'f'


def chord_sharp_or_flat(curr_chord, curr_loop):
    """Takes a chord in a loop and returns whether it should be labelled with notes that are sharp or flat

    @type curr_chord: Chord
    @type curr_loop: Loop
    @rtype: str
        either 's' or 'f'
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
            name = get_chord_name(curr_chord, curr_loop)[:2]
        else:
            name = get_chord_name(curr_chord, curr_loop)[0]
        return key_sharp_or_flat((name, quality))


def choose_chord(current_loop, measure, previous_chord):
    """Determines the next chord for the loop.

    @type current_loop: Loop
    @type measure: int
    @type previous_chord: Chord
    @rtype: Chord
    """
    # first case is for resolving bVII chords and for the first chord in the loop: return Imaj or I-
    if previous_chord is None or measure == 0 or \
            previous_chord.name == 'bVIImaj' or previous_chord.name == 'bVII7':
        if current_loop.key[1] == 'major':
            return diatonic_major.chords[0]
        else:  # loop.key[1] == 'minor'
            return mi_minor.chords[0]

    # resolving V7 (this can probably be removed due to redundancy)
    elif previous_chord.name == 'V7':
        return_lst = [I, I, I, I, VImin]
        if current_loop.tension > 2 and measure != current_loop.measures - 1:
            return_lst.extend([V7ofIV, V7ofIV, V7ofIV])
        return random.choice(return_lst)

    # this case is for making the final block chord in the loop V7 if there is a high rating of dryness
    elif current_loop.tension > 2 and measure == current_loop.measures - 1 and \
            (previous_chord.quality != 'dominant' or previous_chord.name == 'V7/V' or
             previous_chord.name == 'subV7/V'):
        return V

    # dominant resolution
    # case I: V7/bII goes to V or subV7ofI
    # case II: return either a chord 7 semitones below (equivalent to 5 semitones above), 2 semitones above, or one
    # semitone below
    elif previous_chord.quality == 'dominant':
        if previous_chord.name == 'V7ofbII':
            return random.choice(V, V, subV7ofI)
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
                    if previous_chord.name[:5] != 'subV7':
                        return_chords.extend([chord_change, chord_change, chord_change])

                if (previous_chord.interval - chord_change.interval == 10 or
                        previous_chord.interval - chord_change.interval == -2):
                    return_chords.append(chord_change)

                if previous_chord.interval - chord_change.interval == 1 or \
                        previous_chord.interval - chord_change.interval == -11:
                    e = False
                    return_chords.append(chord_change)
                    if previous_chord.name[:5] == 'subV7':
                        return_chords.extend([chord_change, chord_change, chord_change])

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
            chord_selection.extend([chord, chord, chord, chord])
        elif interval == 2:
            chord_selection.extend([chord, chord])
        elif interval == 3:
            chord_selection.extend([chord, chord, chord])
        elif interval == 4:
            chord_selection.extend([chord, chord, chord])
        elif interval == 5:
            chord_selection.extend([chord, chord, chord, chord])
        elif interval == 6:
            chord_selection.extend([chord, chord])

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


def get_chord_name(chord_device, curr_loop):
    """Returns the name of the chord chord_device according to its relation
    to the tonic.

    Used when printing functional chord symbol and relating it to a key.

    @type chord_device: Chord
    @type curr_loop: Loop
    @rtype: str
    """
    key_sorf = key_sharp_or_flat(curr_loop.key)
    tonic = curr_loop.key[0]
    if key_sorf == 's':
        interval = notes_sharp.index(tonic) + chord_device.interval

    else:  # sharp_or_flat == 'f'
        interval = notes_flat.index(tonic) + chord_device.interval

    while interval > 11:
        interval -= 12

    if diatonic(chord_device, curr_loop):
        sharp_or_flat = key_sharp_or_flat(curr_loop.key)
        if sharp_or_flat == 's':
            chosen_notes = notes_sharp
        else:  # sharp_or_flat == 'f'
            chosen_notes = notes_flat
        root = chosen_notes[interval]

    else:
        if curr_loop.key[1] == 'major':
            root = notes_flat[interval]
        else:
            root = notes_sharp[interval]

    quality = chord_device.quality
    if quality == 'dominant':
        quality = '7'
    elif quality == 'major':
        quality = 'maj'
    else:  # quality == 'minor
        quality = '-'
    name = root + quality

    return name


def get_voicing(chord, loop, prev_voice):
    """Calculates and returns a voicing for a chord based on loop's properties

    @type chord: Chord
    @type loop: Loop
    @type prev_voice: str | None
    @rtype: str 'A B C D'
    """
    voicings = set_voicings()

    voicing_options = []
    if chord.quality == 'major':
        num = 0
    elif chord.quality == 'minor':
        num = 1
    else:  # chord.quality == 'dominant'
        num = 2

    sharp_or_flat = chord_sharp_or_flat(chord, loop)
    if sharp_or_flat == 's':
        chosen_notes = notes_sharp
    else:  # sharp_or_flat == 'f'
        chosen_notes = notes_flat

    for voicing in voicings[num]:
        voicing_options.append(voicing)

    if chord.name == 'Imaj':  # removing #4 from possible voicings
        del voicing_options[8]
        del voicing_options[7]
        del voicing_options[4]
    elif chord.name == 'III-':  # also removing #4 from possible voicings
        voicing_options[6].notes[0] = 0
        del voicing_options[4]
        del voicing_options[1]
    elif chord.name == 'V7/II':  # accounting for b13 tension
        voicing_options[1].notes[1] = 8
        voicing_options[3].notes[2] = 8
        voicing_options[4].notes[3] = 8
        voicing_options[4].notes[2] = 6
    elif chord.name == 'V7/III' or chord.name == 'V7/VI' or chord.name == 'V7' and loop.key[1] == 'minor':
        # accounting for b9 and b13 tensions
        voicing_options[1].notes[1] = 8
        voicing_options[3].notes[2] = 8
        voicing_options[3].notes[0] = 1
        voicing_options[4].notes[3] = 8
        voicing_options[4].notes[2] = 6
        voicing_options[4].notes[0] = 1

    candidates = []
    for voice in voicing_options:
        if voice.depth == loop.depth:
            candidates.append(voice)

    voice = random.choice(candidates)

    str_to_return = ''

    if loop.key[0] not in chosen_notes:
        if chosen_notes == notes_sharp:
            temp_chosen_notes = notes_flat
        else:
            temp_chosen_notes = notes_sharp
    else:
        temp_chosen_notes = chosen_notes
    root_value = temp_chosen_notes.index(loop.key[0]) + chord.interval
    if root_value > 11:
        root_value -= 12

    for note in voice.notes:
        new_note = root_value + note
        if new_note > 11:
            new_note -= 12
        str_to_return += chosen_notes[new_note] + ' '

    if prev_voice is not None:
        if loop.depth == 0:
            str_to_return = get_inversion(str_to_return, prev_voice, 2, chord, loop)
        elif loop.depth == 1:
            str_to_return = get_inversion(str_to_return, prev_voice, 3, chord, loop)
        elif 2 <= loop.depth <= 3:
            str_to_return = get_inversion(str_to_return, prev_voice, 4, chord, loop)
        else:  # loop.depth == 4
            str_to_return = get_inversion(str_to_return, prev_voice, 5, chord, loop)

    voices = set_voicings()
    voicings[0] = voices[0]
    voicings[1] = voices[1]
    voicings[2] = voices[2]

    return str_to_return


def get_inversion(two_notes, prev_voice, number_of_voices, curr_chord, curr_loop):
    """Calculates and returns the inversion optional for two-note voice-leading

    @type two_notes: str 'A B'
    @type prev_voice: str
    @type number_of_voices: int
        0 <= number_of_voices <= 4
    @type curr_chord: Chord
    @type curr_loop: Loop
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

    sharp_or_flat = chord_sharp_or_flat(curr_chord, curr_loop)
    if sharp_or_flat == 's':
        chosen_notes = notes_sharp
    else:  # sharp_or_flat == 'f'
        chosen_notes = notes_flat

    # Ensuring there will not be semi-tones at the top of a voice-lead
    if number_of_voices > 3:
        for note_set in note_sets:
            if abs(chosen_notes.index(note_set[2]) - chosen_notes.index(note_set[3])) == 1 \
                    or abs(chosen_notes.index(note_set[0]) - chosen_notes.index(
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
            if first not in chosen_notes:
                first = get_enharmonic(first)
            if second not in chosen_notes:
                second = get_enharmonic(second)
            interval = abs(chosen_notes.index(first)-chosen_notes.index(second))
            if interval > 6:
                interval = 12 - interval
            distances[note_sets.index(note_set)] += interval

    minimum = distances.index(min(distances))
    char3 = ''
    for char in note_sets[minimum]:
        char3 += char + ' '
    return char3


def passing_chords(curr_line, curr_frame, curr_loop):
    """Decorates the loop with passing chords

    @type curr_line: list[(Chord)]
    @type curr_frame: Frame
    @type curr_loop: Loop
    @rtype: None
    """
    if curr_line[0][0].quality == 'dominant':  # 2-5s
        if random.randint(0, 1) == 0:
            interval = curr_line[0][0].interval - 5
            if interval < 0:
                interval += 12
            relative_ii = Chord('relII-', 'minor', interval)

            curr_line[4] = curr_line[0]
            curr_line[0] = (relative_ii, 'relII-', get_chord_name(relative_ii, curr_loop),
                            get_voicing(relative_ii, curr_loop, curr_line[4][3]))

    elif curr_frame.harmony.index(curr_line) == len(curr_frame.harmony) - 1:  # adding turn-around
        if random.randint(0, 2) == 0 and curr_loop.tension >= 2:
            if curr_loop.tension >= 2:
                add_chord = subV7ofI
            else:
                add_chord = bII
            curr_line[6] = (add_chord, add_chord.name, get_chord_name(add_chord, curr_loop),
                            get_voicing(add_chord, curr_loop, curr_line[0][3]))
            if random.randint(0, 1) == 0:
                curr_line[4] = (IImin, 'II-', get_chord_name(IImin, curr_loop),
                                get_voicing(IImin, curr_loop, curr_line[0][3]))

    elif random.randint(0, 1) == 0:  # adding subV7 or V7 with possible 2-5 to prepare for next chord

        next_chord = curr_frame.harmony[curr_frame.harmony.index(curr_line) + 1][0][0]
        curr_chord = None

        if curr_loop.tension < 2:
            chord_options = []
            chord_options.extend(diatonic_major.chords)
            chord_options.extend(diatonic_minor.chords)
            chord_options.extend(mi_major.chords)
            chord_options.extend(mi_minor.chords)

            best_options = []
            for chord_option in chord_options:
                best_options.append(chord_option)
                if 1 <= abs(chord_option.interval - next_chord.interval) <= 2:
                    best_options.extend([chord_option, chord_option])

            chosen_chord = random.choice(best_options)

            curr_line[random.choice([4, 6])] = (chosen_chord, chosen_chord.name,
                                                get_chord_name(chosen_chord, curr_loop),
                                                get_voicing(chosen_chord, curr_loop, curr_line[0][3]))

            if random.randint(0, 1) == 0:
                chosen_chord_2 = random.choice(best_options)
                curr_line[random.choice([4, 6])] = (chosen_chord_2, chosen_chord_2.name,
                                                    get_chord_name(chosen_chord_2, curr_loop),
                                                    get_voicing(chosen_chord_2, curr_loop, curr_line[0][3]))

            return

        for dom in ma_sub_dominant.chords:
            if dom.interval - 1 == next_chord.interval or dom.interval + 11 == next_chord.interval:
                curr_line[6] = (dom, dom.name, get_chord_name(dom, curr_loop), get_voicing(dom, curr_loop,
                                                                                           curr_line[0][3]))
                curr_chord = dom
        for dom in mi_sub_dominant.chords:
            if dom.interval - 1 == next_chord.interval or dom.interval + 11 == next_chord.interval:
                curr_line[6] = (dom, dom.name, get_chord_name(dom, curr_loop), get_voicing(dom, curr_loop,
                                                                                           curr_line[0][3]))
                curr_chord = dom

        if curr_chord is not None:
            interval = curr_chord.interval + 1
            if interval > 11:
                interval -= 12
            relative_ii = Chord('relII-', 'minor', interval)

            curr_line[4] = (relative_ii, 'relII-', get_chord_name(relative_ii, curr_loop),
                            get_voicing(relative_ii, curr_loop, curr_line[0][3]))

        for dom in ma_sec_dom.chords:
            if dom.interval - 7 == next_chord.interval or dom.interval + 5 == next_chord.interval:
                curr_line[6] = (dom, dom.name, get_chord_name(dom, curr_loop), get_voicing(dom, curr_loop,
                                                                                           curr_line[0][3]))
                curr_chord = dom
        for dom in mi_sec_dom.chords:
            if dom.interval - 7 == next_chord.interval or dom.interval + 5 == next_chord.interval:
                curr_line[6] = (dom, dom.name, get_chord_name(dom, curr_loop), get_voicing(dom, curr_loop,
                                                                                           curr_line[0][3]))
                curr_chord = dom

        if curr_chord is not None:
            interval = chord.interval - 5
            if interval < 0:
                interval += 12
            relative_ii = Chord('relII-', 'minor', interval)

            curr_line[4] = (relative_ii, 'relII-', get_chord_name(relative_ii, curr_loop),
                            get_voicing(relative_ii, curr_loop, curr_line[0][3]))


# Chord(name, quality, interval)

I = Chord('Imaj', 'major', 0)
IV = Chord('IVmaj', 'major', 5)

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
    """Resets all voicings
    @rtype: list[list[Voicing]]
    """

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
                      Voicing([2, 3, 7], 1),
                      Voicing([3, 5, 7], 1),
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


# returns 8-note melody for a chord
class Spot:
    """
    Represents a placeholder for a note/rest in a four/four measure

    Attributes:
    @type value: str
        either A, S, or R, or None
    @type index: int
        0 <= index <= 15
    @type note: int | None
        int that represents interval above chord
    """

    def __init__(self, index):
        """Constructs a spot in a measure

        @type self: Spot
        @type index: int
        @rtype: None
        """
        self.value = None
        self.note = None
        self.index = index


def get_melody(harmony, new):
    """Creates and returns the melody for the chord

    @type harmony: list[tuple]
    @type new: bool
    @rtype: list[Spot], list[Spot]
        first list is the notes, second is the rhythm (for repetition/consistency purposes)
    """

    if new:
        rests = assign_rests()
        rhythm = assign_rhythm(rests)
    else:
        rhythm = prev_rhythm

    return_melody = get_notes(rhythm, harmony)

    return return_melody, rhythm


def assign_rests():
    """
    Assigns rests for a four/four measure for a chord

    @rtype: list[Spot]
    """

    spots = []
    for i in range(8):
        spots.append(Spot(i))

    rest_amount = random.randint(0, 2)
    rest_count = 0

    while rest_count < rest_amount:

        for spot in spots:
            if spot.value is None:
                rating = index_rating(spot, spots, rest_amount)
                reference = random.randint(1, 100)
                if reference < rating * 100:
                    spot.value = 'R'
                    rest_count += 1
                    if rest_count == rest_amount:
                        return spots

    return spots


def index_rating(curr, spots, rest_amount):
    """Returns a rating for the likelihood that a spot will be chosen for a rest

    @type curr: Spot
    @type spots: list[Spot]
    @type rest_amount: int
    @rtype: float
    """

    rest_indices = []
    return_val = rest_amount / 8

    for spot in spots:
        if spot.value is not None:
            if spot.index != 0 and spot.index != 1:
                rest_indices.append(spot.index)

    for index in rest_indices:
        for i in range(1, 4):
            if (curr.index * i) % index == 0 or (index * i) % curr.index == 0:
                return_val *= 1.2

        if abs(curr.index - index) == 1:
            return_val *= 1.2

    return return_val


def assign_rhythm(spots):
    """Assigns rhythm values to the spots which are not rests

    @type spots: list[Spot]
    @rtype: list[Spot]
    """

    for spot in spots:
        if spot.value != 'R':
            if spots[spots.index(spot)-1].value == 'R':
                spot.value = 'A'
            elif spots.index(spot) == 0:
                spot.value = 'A'
            elif random.randint(1, 2) == 1:
                spot.value = 'A'
            else:
                spot.value = 'S'

    return spots


def get_notes(spots, chords):
    """Determines notes for each spot in spots

    @type spots: list[Spot]
    @type chords: list[tuple]
    @rtype: list[Spot]
    """

    full_chords = []
    curr = None

    for chord_change in chords:
        if len(chord_change) > 0:
            full_chords.append(chord_change[0])
            curr = chord_change[0]
        else:
            full_chords.append(curr)

    scale_notes = {'guide': [], 'shell': [], 'color': []}

    for spot in spots:
        choices = ['guide', 'shell', 'color']

        if full_chords[spots.index(spot)].quality == 'major':
            scale_notes['guide'] = [4, 11]
            scale_notes['shell'] = [0, 7]
            scale_notes['color'] = [2, 6, 9]
            if full_chords[spots.index(spot)].name == 'Imaj':
                scale_notes['color'].remove(6)
            if loop.depth >= 2:
                scale_notes['shell'].remove(0)
        elif full_chords[spots.index(spot)].quality == 'minor':
            scale_notes['guide'] = [3, 10]
            scale_notes['shell'] = [0, 7]
            scale_notes['color'] = [2, 5, 9]
            if full_chords[spots.index(spot)].name == 'II-':
                scale_notes['color'].remove(9)
            if full_chords[spots.index(spot)].name == 'III-':
                scale_notes['color'].remove(2)
        else:  # full_chords[spots.index(spot)].quality == 'dominant'
            scale_notes['guide'] = [4, 10]
            scale_notes['shell'] = [0, 7]
            scale_notes['color'] = [2, 9]
            if full_chords[spots.index(spot)].name == 'V7/II':
                scale_notes['color'] = [2, 8]
            elif full_chords[spots.index(spot)].name == 'V7/III' or full_chords[spots.index(spot)].name == 'V7/VI':
                scale_notes['color'] = [1, 3, 8]

        if spot.value == 'A':
            if spot.index % 4 == 0:
                choices.extend(['guide', 'guide', 'guide'])
            elif spot.index % 2 == 0:
                choices.extend(['shell', 'shell', 'shell'])
            else:
                choices.extend(['color', 'color', 'color'])

            options = scale_notes[random.choice(choices)]

            if spots.index(spot) == 0:
                spot.note = random.choice(options)
            else:
                delta = 13
                final = None
                prev = spots[spots.index(spot) - 1].note
                count = 2
                while prev is None:
                    prev = spots[spots.index(spot) - count].note
                    count += 1
                    if count > 4:
                        spot.note = random.choice(options)

                for option in options:
                    if abs(option - prev) < delta:
                        delta = abs(option - prev)
                        final = option

                options.extend([final, final, final, final])
                spot.note = random.choice(options)

        elif spot.value == 'S':
            spot.note = spots[spots.index(spot)-1].note

    return spots


def get_note_names(curr_frame, curr_loop):
    """Takes a frame and returns a list of lists containing the letter names of melody notes

    @type curr_frame: Frame
    @type curr_loop: Loop
    @rtype: [[str]]
    """

    return_notes = []
    curr_chord = None

    for line in curr_frame.melody:

        new_notes = []
        count = 0
        for curr_note in line:

            if len(curr_frame.harmony[curr_frame.melody.index(line)][count]) > 0:
                curr_chord = curr_frame.harmony[curr_frame.melody.index(line)][count][0]
                sharp_or_flat = chord_sharp_or_flat(curr_chord, curr_loop)
                if sharp_or_flat == 's':
                    chosen_notes = notes_sharp
                else:  # sharp_or_flat == 'f'
                    chosen_notes = notes_flat

            if curr_note is None:
                new_notes.append(999)
            else:
                # calcluate interval between curr_note and the tonic of the key
                interval = curr_note + curr_chord.interval

                if loop.key[0] not in chosen_notes:
                    if chosen_notes == notes_sharp:
                        temp_chosen_notes = notes_flat
                    else:
                        temp_chosen_notes = notes_sharp
                else:
                    temp_chosen_notes = chosen_notes

                tonic = temp_chosen_notes.index(curr_loop.key[0])
                target = tonic + interval
                while target > 11:
                    target -= 12
                new_notes.append(chosen_notes[target])
            count += 1
        return_notes.append(new_notes)

    return return_notes


if __name__ == "__main__":

    a = True
    while a:
        # primitive UI
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
        frame = Frame()

        previous = None
        previous_voice = None

        # determining the fundamental/block chords
        for measure_counter in range(loop.measures):
            chord = choose_chord(loop, measure_counter, previous)
            previous = chord

            voice = get_voicing(chord, loop, previous_voice)
            previous_voice = voice

            frame.harmony.append([(chord, chord.name, get_chord_name(chord, loop), voice), (), (), (), (), (), (), ()])

        # decorating the loop with passing chords
        for line in frame.harmony:
            passing_chords(line, frame, loop)

        # adding melody
        for line in frame.harmony:
            if frame.harmony.index(line) == loop.measures - 1 or (frame.harmony.index(line) + 1) % 4 == 0 \
                    or frame.harmony.index(line) == 0 or frame.harmony.index(line) % 4 == 0:
                new_rhythm = True
            else:
                new_rhythm = False

            melody = get_melody(line, new_rhythm)
            prev_rhythm = melody[1]
            temp = []
            for note in melody[0]:
                temp.append(note.note)

            frame.melody.append(temp)

        # displaying harmony output
        for line in frame.harmony:
            print(line)

        print()

        # displaying melody output
        for line in frame.melody:
            print(line)

        melody_notes = get_note_names(frame, loop)

        for line in melody_notes:
            print(line)

        again = input('again? (y/n) ')
        print()
        if again == 'n':
            a = False
