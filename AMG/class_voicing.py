"""Contains the class Voicing"""


class Voicing:
    """Represents the particular notes of a four-voice chord

    === Attributes ===
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
