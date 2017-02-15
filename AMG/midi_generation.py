import mido
from mido import MidiFile, MidiTrack, Message
from time import sleep
notes_flat = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']
notes_sharp = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
drum_beats = ['Kick', 'Snare', 'HH']

Midi_Dict = {}
Sharp_Dict = {}

for i, note in enumerate(notes_flat):
	Midi_Dict[note] = 57 + i
for i, note in enumerate(notes_sharp):
	Sharp_Dict[note] = 57 + i

Midi_Dict.update(Sharp_Dict)
Midi_Dict['Rest'] = 0

def find_closest(past, next):
	if past >= next:
		while(True):
			if abs(past - next) > 6:
				next += 12
			else: break
	else:
		while(True):
			if abs(next - past) > 6:
				next -= 12
			else: break
	while(True):
		if next < 60: #middle C two octaves
			next += 12
		elif next > 84:
			next -= 12
		else:
			return next


def generate_track(note_array, channel, octave=0, program=0, velocity = 64, drums = False):
	from amg import Note
	time = 512
	track = MidiTrack()
	pastnote = Midi_Dict[note_array[0].value]
	track.append(Message('program_change', program = program, channel = channel))
	for note in note_array:
		if note.value == 'Rest':
			track.append(Message('note_on', channel=channel, note=Midi_Dict[note.value] + octave * 12, velocity=0, time=1))
			track.append(Message('note_off', channel=channel, note=Midi_Dict[note.value] + octave * 12, velocity=0, time=time*note.length))
		else:
			pastnote = find_closest(pastnote, Midi_Dict[note.value])
			track.append(Message('note_on', channel=channel, note=pastnote + (octave * 12), velocity = velocity, time=1))
			track.append(Message('note_off', channel=channel, note=pastnote + (octave * 12), velocity=velocity, time=time*note.length))
	track += track *7
	return track

def combine_tracks(track_array):
	mid = MidiFile(type=1)
	for track in track_array:
		mid.tracks.append(track)
	return mid