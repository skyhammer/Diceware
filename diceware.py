########################################################################################################################
# Author: David Cartwright
# Date: 01 May 2015
# Version: 0.1
#
# This software is the back-end to produce a secure passphrase using the Diceware Method, developed by Arnold G.
# Reinhold, Cambridge, Massachusetts, USA. Copyright © 1995-2015
#
# The English Diceware Wordlist used with this software ("diceware.wordlist") is licensed by Arnold G.
# Reinhold under the `Creative Commons CC-BY 3.0` (see http://creativecommons.org/licenses/by/3.0/) license.
#
# "Diceware" is a trademark of A G Reinhold.
#
# Changelog
# =========
#
# 0.1 29/01/2015 - Initial Release
########################################################################################################################

# Import Modules
from random import SystemRandom
import os


class Diceware:
    """A Class that creates an object for creating cryptographically safe random numbers."""

    def __init__(self):

        # Use the OS specific function to generate random numbers for greater security
        self.cryptogen = SystemRandom()
        self.cryptolist = list()

    def dice_roll(self, start=1, end=6, num_range=5):
        """Creates a list of numbers with a given range.

        Keyword arguments:
        start     -- the start of the number range (default is 1)
        end       -- the end of the number range (default is 6)
        num_range -- the length of the list of numbers to generate (default is 5)
        """

        # The randrange function takes a starting number and goes up to, but does not include the end number
        # so let's add 1 to the end number to include it.
        self.cryptolist = [self.cryptogen.randrange(start, (end + 1)) for i in range(num_range)]

    def word_lookup(self):
        """Creates a string from the cryptographically safe list of numbers, which is used to search the diceware
        word list file.
        """

        # Make sure we start with an empty string
        self.num_to_string = ""

        # Iterate through the list, adding each number to the string
        for i in self.cryptolist:
            self.num_to_string += str(i)

        # We'll try and open the diceware word list file, search it, then return the word
        try:
            with open("diceware.wordlist", "r") as handler:
                for line in handler:
                    if self.num_to_string in line:
                        # Return only the word, removing the numbers and whitespace
                        return line[len(self.num_to_string):].strip()

        except FileNotFoundError:
            # Whoops, the diceware word list cannot be found
            print("Unable to open " + str(os.getcwd()) + "\diceware.wordlist - File not found.")


if __name__ == '__main__':
    app = Diceware()
