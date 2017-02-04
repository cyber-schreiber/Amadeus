import mido
from mido import MidiFile, MidiTrack, Message	

notes_flat = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']
notes_sharp = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']

Midi_Dict = {}
Sharp_Dict = {}

for i, note in enumerate(notes_flat):
	Midi_Dict[note] = 57 + i
for i, note in enumerate(notes_sharp):
	Sharp_Dict[note] = 57 + i

Midi_Dict.update(Sharp_Dict)
Midi_Dict['Rest'] = 0


def generate_measure_track(melodyarray):
	track = MidiTrack()
	i = 0	
	while i < len(melodyarray):
		time = 256
		note = melodyarray[i]
		while i < len(melodyarray) - 1 and melodyarray[i] == melodyarray[i + 1]:
			i += 1
			time += 256
		if note == 'Rest':
			track.append(Message('note_on', note=Midi_Dict[note], velocity=0, time=256))
			track.append(Message('note_off', note=Midi_Dict[note], velocity=0, time=256))
		else:
			track.append(Message('note_on', note=Midi_Dict[note], velocity=64, time=time))
   			track.append(Message('note_off', note=Midi_Dict[note], velocity=64, time=time))
   		i += 1		
	return track

def create_melody_track(melody):
	sum_melody = sum(melody,[])
	track = generate_measure_track(sum_melody)
	return track



def create_chord_tracks_measure(chord_notes, depth):
	


def create_chord_Track(chords):
	sum_chords = sum(chords)
	tracks = generate_measure_track(sum_chords)
	return tracks



# def chord


mellow = [['Rest', 'G', 'F', 'F', 'F', 'Bb', 'Bb', 'C'], ['G', 'G', 'Eb', 'Rest', 'G', 'F', 'F', 'F']]

melo = create_melody_track(mellow)
for i in range(8):
	melo += melo
mid = MidiFile()
mid.tracks.append(melo)
mid.save("new_song.mid")