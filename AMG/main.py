"""Main code for Amadeus -> creates, writes, and plays a Loop ~ """

from class_loop import *
import random
import random
import mido
import pygame
from midi_generation import generate_track, combine_tracks
from playnotes import play_music
from io import BytesIO
import os
import time


def run_amadeus():
    """Runs this shit, oh yeaaa ~ """

    intensity = None

    a = True
    while a:
        a = False
        intensity = input('How chill of a listening experience would you like? '
                          '(very chill, chill, in between, intense, very intense) ')

        if intensity in ['very chill', '0']:
            intensity = 0
        elif intensity in ['chill', '1']:
            intensity = 1
        elif intensity in ['in between', '2']:
            intensity = 2
        elif intensity in ['intense', '3']:
            intensity = 3
        elif intensity in ['very intense', '4']:
            intensity = 4
        else:
            a = True

    curr_loop = Loop(random.choice([2, 4, 8]), intensity)
    curr_loop.write_loop()

    for output in [curr_loop.harm['passing'], curr_loop.melody['notes'], curr_loop.bass['notes']]:
        # print(output)
        pass

    for output in curr_loop.perc:
        if output != 'final':
            # print(curr_loop.perc[output])
            pass

    return curr_loop


if __name__ == '__main__':
    loop = run_amadeus()

    tracks = []

    # displaying harmony output

    # for line in harmony_note_objects(frame):
    #     for notes in line:
    #         for note in notes:
    #             print(note)
    #         print()

    harmony_notes = loop.harm['final'].measures
    melo_note_o_0 = loop.melody['final'].measures
    new_bass_notes = loop.bass['final'].measures

    flattened_0 = [val for val in harmony_notes]
    flattened = []
    for measure in flattened_0:
        flattened.append(measure.notes)
    # print(flattened)

    melo_note_o_1 = [val for val in melo_note_o_0]
    melo_note_o = []
    for measure in melo_note_o_1:
        melo_note_o.append(measure.notes)

    for measure in flattened:
        for i, chord in enumerate(measure):
            new_chord = []
            prev_char = ''
            # print(chord.value)
            for char in chord.value['voicing']:
                if char == ' ':
                    new_chord.append(Note(prev_char, chord.length, chord.index))
                    prev_char = ''
                else:
                    prev_char += char
            measure[i] = new_chord
    # print(flattened)

    for note in flattened:
        for nott in note:
            print(nott)
    ordered = []
    for i in range(len(flattened[0])):
        line_seq = []
        for line in flattened:
            # print(i)
            line_seq.append(line[i])
        for note in line_seq:
            print(note)
        ordered.append(line_seq)

    # simple drum pattern
    drums = []
    kicknote = Note('C', 1, 0)
    hhnote = Note('Gb', 1, 0)
    snarenote = Note('E', 1, 0)
    drums = [kicknote, hhnote, snarenote, hhnote]
    for i in range(0, 2):
        drums.extend(drums)

    # chosing instruments
    chords_program = random.randint(41, 44)
    melo_program = random.randint(81, 96)
    bass_program = random.randint(33, 40)

    # creating track
    tracks.append(generate_track(drums, 9, octave=-2))
    tracks.append(generate_track(melo_note_o, 10, program=melo_program, velocity=64))
    tracks.append(generate_track(new_bass_notes, 11, octave=-3, program=bass_program, velocity=64))
    for i, notes in enumerate(ordered):
        for note in notes:
            print(note)
        print()
        if i == 0:
            tracks.append(generate_track(notes, i, octave=0, program=chords_program, velocity=45))
        else:
            tracks.append(generate_track(notes, i, octave=-1, program=chords_program, velocity=45))

    # melody_notes = get_note_names(frame, loop, False)

    # combining and playing music
    print("combining")
    melody_midi = combine_tracks(tracks)
    pygame.init()
    melody_midi.save("melo.mid")
    pygame.mixer.music.load("melo.mid")

    pygame.mixer.music.play()
    on = True
    while on:
        again = input('play again? (y/n) ')
        print()
        if again == 'y':
            pygame.mixer.music.play()
        else:
            on = False

    again = input('save midi? (y/n) ')
    print()

    if again == 'y':
        filename = input('what name you want to give to this dope ass beat: \n')
        os.rename("melo.mid", filename)

    again = input('again? (y/n) ')

    if again == 'n':
        a = False
