"""Contains Measure class, which is comprised of Notes"""

from class_note import *
import random


class Measure:
    """Represents one measure in a loop's Frame, and is comprised of Note objects ~

    === Attributes ===
    @type length: int
    @type notes: list[Note]
    @type prev: Measure | None
    @type next: Measure | None
    """

    def __init__(self, length, index):
        """Constructs an empty Measure of Notes with attribute (value -> None) ~

        @type self: Measure
        @type length: int
        @type index: int
            index of the first note of this measure
        @rtype: None
        """
        self.length = length
        self.notes = []
        self.prev = None
        self.next = None

        prev_note = None
        curr_note = Note(None, 1, 0)
        next_note = Note(None, 1, index+1)

        for _ in range(length):
            curr_note.prev = prev_note
            curr_note.next = next_note
            curr_note.index = index

            self.notes.append(curr_note)

            prev_note = curr_note
            curr_note = next_note
            next_note = Note(None, 1, index+1)

            index += 1

        if prev_note is not None:
            prev_note.next = None
