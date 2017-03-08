"""Contains Frame class, which is comprised of Measures ~ """

from class_measure import *


class Frame:
    """Represents one element of a loop, and is comprised of Measure objects ~

    === Attributes ===
    @type length: int
    @type measures: list[Measure]
    """

    def __init__(self, length):
        """Constructs an empty Frame comprised of empty Measures ~

        @type self: Frame
        @type length: int
        @rtype: None
        """

        self.length = length
        self.measures = []
        counter = 0

        prev_measure = None
        curr_measure = Measure(8, counter)
        next_measure = Measure(8, counter+8)
        # 8 means 1/8 notes; this will be upgraded to apply to variable divisions of a measure

        for _ in range(length):
            counter += 8

            curr_measure.prev = prev_measure
            curr_measure.next = next_measure

            self.measures.append(curr_measure)

            prev_measure = curr_measure
            curr_measure = next_measure
            next_measure = Measure(8, counter+8)

        if prev_measure is not None:
            prev_measure.next = None

        # Linking notes at the end/start of measures
        for curr_measure in self.measures:
            for curr_note in curr_measure.notes:
                if (curr_note.index+1) % length == 0 and curr_note.index+1 != 8*length:
                    end_note = curr_note
                if curr_note.index % length == 0 and curr_note.index != 0:
                    curr_note.prev = end_note
                    end_note.next = curr_note

    def __str__(self):
        """Prints the values of a Frame

        @type self: Frame
        @rtype: None
        """

        for curr_measure in self.measures:
            display = []
            for curr_note in curr_measure.notes:
                display.append((curr_note.value, curr_note.length))
            print(display)
        print()

        return ''

    def extend(self):
        """Returns an new Frame which is extended version of a Frame (self) ~

        @type self: Frame
        @rtype: Frame
        """

        new_frame = Frame(1)
        new_notes = []

        for curr_measure in self.measures:
            new_notes.extend(curr_measure.notes)

        new_frame.measures = [Measure(0, self.length)]
        new_frame.measures[0].notes = new_notes

        return new_frame

    def collapse(self, curr_loop):
        """Returns a new Frame which is a collapsed version of a previously extended Frame (self) ~

        @type self: Frame
        @type curr_loop: Loop
        @rtype: Frame
        """

        new_frame = Frame(curr_loop.measures)
        counter = 0

        for curr_measure in new_frame.measures:
            for curr_note in curr_measure.notes:
                curr_note.value = self.measures[0].notes[counter].value
                counter += 1

        return new_frame

    def __getitem__(self, index):
        """Returns the Note at the specified index of (extended form of) a Frame (self) ~

        @type self: Frame
        @type index: int
        @rtype: Note
        """

        return self.extend().measures[0].notes[index]

    def compress(self):
        """Returns a new Frame whose adjacent notes of equivalent value have been combined ~
        This also mutates the original Frame ~

        @type self: Frame
        @rtype: Frame
        """
        new_frame = Frame(self.length)
        new_frame.measures = self.measures
        prev_note = None

        for i, curr_measure in enumerate(new_frame.measures):
            new_measure = []
            length = 1

            for curr_note in curr_measure.notes:

                # If curr_note is not the final note in the loop
                if curr_note.next is not None:

                    # If the next note has the same value as curr_note, add 1 to length and consider next note
                    if curr_note.value == curr_note.next.value and (curr_note.index+1) % 8 != 0:
                        curr_note.next = curr_note.next.next
                        length += 1

                    # For final note of same value as prev notes, add note with accumulated length to new_measure
                    else:
                        curr_note.length = length
                        curr_note.index += 1-length
                        curr_note.prev = prev_note
                        new_measure.append(curr_note)
                        length = 1
                        prev_note = curr_note

                # Dealing with the final note in the loop, as its 'next' attribute is None
                else:
                    curr_note.length = length
                    curr_note.index += 1 - length
                    curr_note.prev = prev_note
                    new_measure.append(curr_note)
                    length = 1
                    prev_note = curr_note

            # Dealing with adjacent measures having the same first/last notes -> for now, they are split
            if length > 1:
                curr_note.length = length
                curr_note.index += 1 - length
                curr_note.prev = prev_note
                new_measure.append(curr_note)
                prev_note = curr_note

            final_measure = Measure(8, 0)
            final_measure.notes = new_measure
            new_frame.measures[i] = final_measure

        return new_frame


if __name__ == '__main__':
    frame = Frame(4)
    print(frame)
    print(frame.extend())
    print(frame.extend().collapse())
