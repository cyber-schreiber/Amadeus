"""Contains class Loop, which is comprised of Measures ~ """

from harmony_frames import *
from melody_frames import *
from bass_frames import *
from perc_frames import *
from class_frame import *
import random


class Loop:
    """Represents one loop, which is comprised of a shitload of Frame objects ~

    === Attributes ===
    @type melody: dict{str: Frame}
        contains keys: 'rhythm', 'ints', 'notes', 'final'
    @type bass: dict{str: Frame}
        contains keys: 'rhythm', 'ints', 'notes', 'final'
    @type perc: dict{str: Frame}
        contains keys: 'kick', 'snare', 'closed_hat', 'open_hat', 'final'
    @type harm: dict{str: Frame}
        contains keys: 'shell', 'passing', 'rhythm', 'final'

    @type rhythm_ref: list[int]
        e.g. [1, 0, 0, 1, 0, 0, 1, 0], where 1's are salient and 0's are not; ref is short for reference

    @type measures: int
    @type key: dict{'root': str (e.g. 'Ab'), 'quality': str (e.g. 'major')}
    @type attributes: dict{attribute str: value int}
        contains variables for compositional variety, e.g. conjunct/disjunct melody, deep/shallow harmony,
        degree of activity of bassline/percussion, etc.
    """

    def __init__(self, measures, intensity):
        """Constructs an empty Loop ~

        @type self: Loop
        @type measures: int
        @rtype: None
        """
        # Assigning fundamental/invariable attributes
        self.measures = measures
        self.key = None
        self.attributes = {}
        self.rhythm_ref = None

        self.write_key()
        self.write_attributes(intensity)

        # Creating empty Frame objects for variable attributes melody, bass, perc, harmony
        self.melody = {'rhythm': Frame(measures), 'ints': Frame(measures),
                       'notes': Frame(measures), 'final': Frame(measures)}
        self.bass = {'rhythm': Frame(measures), 'ints': Frame(measures),
                     'notes': Frame(measures), 'final': Frame(measures)}
        self.perc = {'kick': Frame(measures), 'snare': Frame(measures), 'closed_hat': Frame(measures),
                     'open_hat': Frame(measures), 'final': Frame(measures)}
        self.harm = {'shell': Frame(measures), 'passing': Frame(measures),
                     'rhythm': Frame(measures), 'final': Frame(measures)}

    def write_key(self):
        """Chooses a random key for a Loop (self) ~

        @type self: Loop
        @rtype: None
        """

        key = None
        onward = False
        while not onward:
            if random.randint(0, 1) == 0:  # flat key
                key = {'root': notes_flat[random.randint(0, 11)], 'quality': 'major'}
                if key['root'] != 'Gb':
                    onward = True
            else:  # sharp key
                key = {'root': notes_sharp[random.randint(0, 11)], 'quality': 'minor'}
                if key['root'] != 'A#' and key['root'] != 'D#':
                    onward = True

        self.key = key

    def write_attributes(self, intensity):
        """Takes a Loop (self) and an intensity rating, and writes its attributes parameter ~
        This is a mutating function ~

        @type self: Loop
        @type intensity: int
        @rtype: None
        """

        self.attributes['depth'] = intensity + random.randint(-1, 1)
        self.attributes['tritone'] = intensity + random.randint(-1, 1)

        for attribute in self.attributes:
            if self.attributes[attribute] == 5:
                self.attributes[attribute] = 4

            if self.attributes[attribute] == -1:
                self.attributes[attribute] = 0

    def write_loop(self):
        """Takes an empty Loop (self) and fills its melody, bass, perc, and harm Frames ~
        This is a mutating function ~
        It is necessary to construct rhythm reference and harmony *before* melody, bass, and percussion ~

        @type self: Loop
        @rtype: None
        """

        self.create_rhythm_ref()
        construct_harmony(self)

        construct_melody(self)
        construct_bass(self)
        construct_percussion(self)

    def create_rhythm_ref(self):
        """Takes a Loop, empty or otherwise, and writes its rhythm_ref ~
        This is a mutating function ~

        @type self: Loop
        @rtype: None
        """

        return_lst = [0, 0, 0, 0, 0, 0, 0, 0]
        hits_total = random.choice([1, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4])
        hit_count = 0

        while True:
            for i, hit in enumerate(return_lst):
                if hit_count == hits_total:
                    self.rhythm_ref = return_lst
                    return

                if random.randint(0, 100) == 77:  # high number of 100 was chosen to decrease bias toward front of list
                    return_lst[i] = 1
                    hit_count += 1


if __name__ == '__main__':
    frame = Frame(8)

    full_notes = []
    for measure in frame.measures:
        notes = []
        for note in measure.notes:
            if note.prev is not None:
                print(note.prev.value)
            notes.append(note.value)
            print(note.value)
            if note.next is not None:
                print(note.next.value)
            print()
        full_notes.append(notes)

    for line in full_notes:
        print(line)

    print()
    count = 0
    for measure in frame.compress().measures:
        notes = []
        for note in measure.notes:
            if note.prev is None:
                prev_value = None
            else:
                prev_value = note.prev.value
            if note.next is None:
                next_value = None
            else:
                next_value = note.next.value
            notes.append((note.value, note.length, note.index, prev_value, next_value))
            count += 1
        print(notes)
