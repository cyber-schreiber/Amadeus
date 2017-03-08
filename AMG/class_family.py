"""
Contains Family class ~

Important attribute is 'chords', which is a tuple of chords belonging to the family ~
"""


class Family:
    """Represents a chord family which has a name and tension/depth ratings ~

    === Attributes ===
    @type name: str
    @type chords: (Chord, Chord, ...)
    @type tritone: int
    @type weight: int
    """

    def __init__(self, name, chords, tritone):
        """Constructs a chord family ~

        @type self: Family
        @type name: str
        @type chords: (Chord, Chord, ...)
        @type tritone: int
        @rtype: None
        """

        self.name = name
        self.chords = chords
        self.tritone = tritone
        self.weight = 0

    def determine_weight(self, curr_loop):
        """Determines the weight of family self based on loop settings ~
        Mutates self's weight attribute accordingly ~

        @type self: Family
        @type curr_loop: Loop
        @rtype: None
        """

        # Arbitrary general formula found through trial and error; though effective, this can probably be improved
        self.weight = int(15 - ((self.tritone - curr_loop.attributes['tritone']) ** 2 * 2.5))

        # Accounting for exceptional chords
        if curr_loop.key['quality'] == 'major':

            # Diatonic chords e.g. I, IV, II- will occur occasionally in high tritone loops, rather than never
            if self.name == 'primary_dominant' or self.name == 'diatonic major' or self.name == 'diatonic minor':
                if curr_loop.attributes['tritone'] > 2:
                    self.weight = 2

            # V7 and bVII7 -> if tritone rating is: (0-1) -> never occur; (2-4) -> occur sporadically
            if self.name == 'mi_dominant' or self.name == 'primary_dominant':
                if curr_loop.attributes['tritone'] < 2:
                    self.weight = 0
                else:  # curr_loop.attributes['tension'] > 2
                    self.weight = 2

            # V7/bII and V7/bVI will occur rarely in major keys
            if self.name == 'mi_sec_dom':
                self.weight = 1

        else:  # loop.key['quality'] == 'minor'

            # Diatonic chords e.g. I-, IV-, bIII will occur occasionally in high tritone loops, rather than never
            if self.name == 'mi_minor' or self.name == 'mi_major':
                self.weight = 2

            # Chord diatonic to major key will occur rarely
            if self.name == 'diatonic major' or self.name == 'diatonic minor' or self.name == 'ma_sec_dom':
                self.weight = 1
