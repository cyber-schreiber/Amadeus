"""Contains Note class, which cannot be broken down further. Note objects are used for output/interface ~ """


class Note:
    """Represents one note in a measure ~

    === Attributes ===
    @type length: int
        Unit is determined by Loop attributes, i.e. 1/8th vs 1/16th notes
    @type index: int
        Represents index of Note in *extended* Frame, i.e. from the start of the Loop
    @type value: obj
    @type prev: Note | None
    @type next: Note | None
    """

    def __init__(self, value, length, index, prev=None, next_note=None):
        """Constructs a Note; prev and next attributes are by default EMPTY ~

        @type self: Note
        @type value: object
            may be int, char, list, str, etc.
        @type length: int
            in decompressed Frames, length = 1. in compressed Frames, length >= 1
        @type index: int
        """
        self.value = value
        self.length = length
        self.index = index
        self.prev = prev
        self.next = next_note
