"""Contains code which determines possible voicings ~

Selects the best available voicing based on voice-leading principles ~
"""

from functions import *
import random


def get_voicing(curr_chord, curr_loop, prev_voice):
    """Calculates and returns a voicing for a chord based on loop's properties ~

    @type curr_chord: Chord
    @type curr_loop: Loop
    @type prev_voice: str | None
    @rtype: str 'A B C D'
    """

    # Reset voicings
    voicings = set_voicings()

    # Determining which voicings will be available based on quality of chord
    voicing_options = []
    if curr_chord.quality == 'major':
        voicings_index = 0
    elif curr_chord.quality == 'minor':
        voicings_index = 1
    else:  # curr_chord.quality == 'dominant'
        voicings_index = 2

    for voicing in voicings[voicings_index]:
        voicing_options.append(voicing)

    # Determining # or b for style
    chosen_notes = chord_sharp_or_flat(curr_chord, curr_loop)

    # Identifying chords with voicing exceptions and altering the available voicings accordingly
    if curr_chord.name == 'Imaj':  # removing #4
        del voicing_options[8]
        del voicing_options[7]
        del voicing_options[4]

    elif curr_chord.name == 'III-':  # also removing scale degree #4
        voicing_options[5].notes[0] = 0
        del voicing_options[3]

    elif curr_chord.name == 'V7/II':  # 13 -> b13
        voicing_options[1].notes[1] = 8
        voicing_options[3].notes[2] = 8
        voicing_options[4].notes[3] = 8
        voicing_options[4].notes[2] = 6

    elif curr_chord.name in ['V7/III', 'V7/VI'] or curr_chord.name == 'V7' and curr_loop.key['quality'] == 'minor':
        # 9 -> b9 or #9, and 13 -> b13
        voicing_options[1].notes[1] = 8
        voicing_options[3].notes[2] = 8
        voicing_options[3].notes[0] = random.choice([1, 3])
        voicing_options[4].notes[3] = 8
        voicing_options[4].notes[2] = 6
        voicing_options[4].notes[0] = random.choice([1, 3])

    elif curr_chord.name == ['relII-7b5', 'II-7b5']:  # turning 5 into b5, and 13 into b13
        voicing_options[0].notes[1] = 6
        voicing_options[1].notes[2] = 6
        voicing_options[2].notes[2] = 6
        voicing_options[3] = Voicing([3, 6, 8, 10], 3)
        voicing_options[4].notes[2] = 6
        voicing_options[5] = Voicing([3, 5, 6, 8, 10], 4)

    # Eliminating voicings with different depth values than curr_loop
    candidates = []
    for voice in voicing_options:
        if voice.depth == curr_loop.attributes['depth']:
            candidates.append(voice)

    voice = random.choice(candidates)

    # Constructing the string to be returned -> arbitrary; only a matter of formatting
    str_to_return = ''

    if curr_loop.key['root'] not in chosen_notes:
        if chosen_notes == notes_sharp:
            temp_chosen_notes = notes_flat
        else:
            temp_chosen_notes = notes_sharp
    else:
        temp_chosen_notes = chosen_notes

    root_value = (temp_chosen_notes.index(curr_loop.key['root']) + curr_chord.interval) % 12

    for curr_note in voice.notes:
        str_to_return += chosen_notes[(root_value + curr_note) % 12] + ' '

    if prev_voice is not None:
        if curr_loop.attributes['depth'] == 0:
            str_to_return = get_inversion(str_to_return, prev_voice, 2, curr_chord, curr_loop)
        elif curr_loop.attributes['depth'] == 1:
            str_to_return = get_inversion(str_to_return, prev_voice, 3, curr_chord, curr_loop)
        elif 2 <= curr_loop.attributes['depth'] <= 3:
            str_to_return = get_inversion(str_to_return, prev_voice, 4, curr_chord, curr_loop)
        else:  # curr_loop.attributes['depth'] == 4
            str_to_return = get_inversion(str_to_return, prev_voice, 5, curr_chord, curr_loop)

    # # Reset voicings
    # voices = set_voicings()
    # voicings[0] = voices[0]
    # voicings[1] = voices[1]
    # voicings[2] = voices[2]

    return str_to_return


def get_inversion(curr_voice, prev_voice, number_of_voices, curr_chord, curr_loop):
    """Calculates and returns the inversion optional for two-note voice-leading ~

    @type curr_voice: str e.g. 'A B C '
    @type prev_voice: str
    @type number_of_voices: int
        0 <= number_of_voices <= 4
    @type curr_chord: Chord
    @type curr_loop: Loop
    @rtype: str e.g. 'A B C '
    """

    # Setting up list of distances, which will be calculated and the smallest of which will be chosen
    distances = []
    for _ in range(number_of_voices):
        distances.append(0)

    # Dividing curr_voice and prev_voice into lists of note names e.g. 'Ab', with empty characters (' ') as boundaries
    curr_characters = []
    char1 = ''
    for char in curr_voice:
        if char != ' ':
            char1 += char
        else:
            curr_characters.append(char1)
            char1 = ''

    prev_characters = []
    char2 = ''
    for char in prev_voice:
        if char != ' ':
            char2 += char
        else:
            prev_characters.append(char2)
            char2 = ''

    # Setting up list of potential voicings, which are made by shuffling characters in curr_voice
    note_sets = [curr_characters]
    for i in range(1, number_of_voices):
        note_sets.append(curr_characters[i:] + curr_characters[:i])

    # if number_of_voices == 2:
    #     note_sets = [curr_characters, curr_characters[1:] + curr_characters[:1]]
    # elif number_of_voices == 3:
    #     note_sets = [curr_characters, curr_characters[1:] + curr_characters[:1],
    #                  curr_characters[2:] + curr_characters[:2]]
    # elif number_of_voices == 4:
    #     note_sets = [curr_characters, curr_characters[1:] + curr_characters[:1],
    #                  curr_characters[2:] + curr_characters[:2],
    #                  curr_characters[3:] + curr_characters[:3]]
    # else:  # number_of_voices == 5
    #     note_sets = [curr_characters, curr_characters[1:] + curr_characters[:1],
    #                  curr_characters[2:] + curr_characters[:2],
    #                  curr_characters[3:] + curr_characters[:3],
    #                  curr_characters[4:] + curr_characters[:4]]

    # Chord name has either # or b
    chosen_notes = chord_sharp_or_flat(curr_chord, curr_loop)

    # Ensuring there will not be semi-tones at the top or bottom of a voicing by increasing pertinent element of
    # distances list beyond being a possible minimum value; 100 was semi-arbitrarily chosen for increase value
    if number_of_voices > 3:
        for note_set in note_sets:
            if abs(chosen_notes.index(note_set[2]) - chosen_notes.index(note_set[3])) == 1 \
                    or abs(chosen_notes.index(note_set[0]) - chosen_notes.index(note_set[1])) == 1:
                distances[note_sets.index(note_set)] += 100

    # Determining the voicing with lowest overall distance from the previous voicing
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

    # Formatting string to return -> this is arbitrary and may be changed/improved
    char3 = ''
    for char in note_sets[minimum]:
        char3 += char + ' '
    return char3
