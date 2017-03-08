""" Contains class Chord ~ """


class Chord:
    """Represents a chord ~

    === Attributes ===
    @type name: str
    @type quality: str
        either major, minor, or dominant
    @type interval: int
        the distance (in semi-tones) between this chord's root and the tonic
    """

    def __init__(self, name, quality, interval):
        """Constructs a Chord ~

        @type self: Chord
        @type name: str
        @type quality: str
        @type interval: int
        @rtype: None
        """

        self.name = name
        self.quality = quality
        self.interval = interval
