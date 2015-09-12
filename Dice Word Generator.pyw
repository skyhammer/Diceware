#!/usr/bin/env python3
########################################################################################################################
# Author: David Cartwright
# Date: 30 August 2015
# Version: 0.2
#
# This software is the front-end GUI to produce a secure passphrase using the Diceware Method, developed by Arnold G.
# Reinhold, Cambridge, Massachusetts, USA. Copyright © 1995-2015
#
# The English Diceware Word list used with this software ("diceware.wordlist") is licensed by Arnold G.
# Reinhold under the `Creative Commons CC-BY 3.0` (see http://creativecommons.org/licenses/by/3.0/) license.
#
# "Diceware" is a trademark of A G Reinhold.
#
# Changelog
# =========
#
# 0.2 30/08/2015 - Improvements to UI (added new options, added copy to clipboard button)
#                - Added a random number and or capitalisation substition option
#
# 0.1 01/05/2015 - Initial Release
########################################################################################################################

# Import Modules
from tkinter import *
from tkinter import ttk
from random import SystemRandom
import string
from diceware import Diceware

# Software Information
VERSION = "0.2"
TITLE = "Diceware Passphrase Generator"

LETTER_TO_NUMBER = {"a": "4", "b": "8", "e": "3", "g": "9", "i": "1", "o": "0", "s": "5", "t": "7", "z": "2"}


class InputFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        self.input_frm = ttk.LabelFrame(self, text="Configuration: ")
        self.input_frm.pack(side=TOP, fill=BOTH)

        # Create a frame to make the widgets look nice
        self.frame1 = Frame(self.input_frm)
        self.frame1.pack(side=TOP, fill=BOTH)

        # Create an options frame
        self.frame2 = Frame(self.input_frm)
        self.frame2.pack(side=BOTTOM, fill=BOTH)

        ttk.Label(self.frame1, text="Number of Words: ").pack(side=LEFT)

        # Create a spinbox, with a range of 1 to 10, and then set the default to 5
        self.num_of_words = StringVar()
        self.word_count = Spinbox(self.frame1, from_=1, to=10, textvariable=self.num_of_words)
        self.word_count.pack(side=LEFT, padx=5, pady=5)
        self.word_count.delete(0, END)
        self.word_count.insert(0, 5)

        # Create the 'Generate' button and give it focus
        self.generate_btn = ttk.Button(self.frame1, text=" Generate\nPassphrase",
                                       command=lambda self=self: Passphrase().get_passphrase(self))
        self.generate_btn.pack(side=RIGHT, padx=5, pady=5)
        self.generate_btn.focus_set()

        # Create the 'options' checkbox widget
        self.opt_allow_num = IntVar()
        self.allow_numbers = ttk.Checkbutton(self.frame2, text="Random Replacement of Numbers for Letters (e.g., A -> 4, S -> 5, etc)",
                                             variable=self.opt_allow_num)
        self.allow_numbers.grid(column=0, row=0, sticky=W)

        self.opt_allow_caps = IntVar()
        self.allow_caps = ttk.Checkbutton(self.frame2, text="Random Capitalisation", variable=self.opt_allow_caps)
        self.allow_caps.grid(column=0, row=1, sticky=W)

        self.generate_btn.bind('<Return>', lambda self=self: Passphrase().get_passphrase(self))

        # Add some padding
        for child in self.frame1.winfo_children():
            child.pack_configure(padx=5, pady=5)

        for child in self.frame2.winfo_children():
            child.grid_configure(padx=5, pady=5)


class OutputFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        self.output_frm = ttk.LabelFrame(self, text="Output: ")
        self.output_frm.pack(side=TOP, fill=BOTH)

        ttk.Label(self.output_frm, text="Passphrase: ").pack(side=LEFT)

        # Create the entry box for the generated passphrase
        self.passphrase = StringVar()
        self.passphrase_entry = ttk.Entry(self.output_frm, textvariable=self.passphrase, width=60)
        self.passphrase_entry.pack(side=LEFT)

        self.copy_btn = ttk.Button(self.output_frm, text=" Copy to\nClipboard", command=self.copy_button)
        self.copy_btn.pack(side=RIGHT)

        # Add some padding
        for child in self.output_frm.winfo_children():
            child.pack_configure(padx=5, pady=5)

    def copy_button(self):
        clip = Tk()
        clip.withdraw()
        clip.clipboard_clear()
        clip.clipboard_append(self.passphrase_entry.get())
        # clip.update()  # calling update() should stop command line apps from freezing. Does not seem to effect the GUI though
        clip.destroy()


class CloseButton(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        ttk.Button(self, text="Quit", command=root.destroy).pack(side=BOTTOM)


class App(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.input_frame = InputFrame(root)
        self.output_frame = OutputFrame(root)
        self.close_button = CloseButton(root)

        self.close_button.pack(side=BOTTOM, padx=5, pady=5)
        self.input_frame.pack(side=TOP, fill=BOTH, padx=5, pady=5)
        self.output_frame.pack(side=BOTTOM, fill=BOTH, padx=5, pady=5)


class Passphrase:
    """
    The Passphrase class contains all the functions to generated a new passphrase and process it, returning the final
    result to the UI
    """
    def __init__(self):
        self.passphrase = str()
        self.word_list = list()
        self.crypt_gen = Diceware()

    def get_passphrase(self, event=None):
        """
        Main part of the program that gets the passphrase, processes it (number substitution & capitalisation),
        then displays the result in the UI
        """

        # Ensure that the passphrase box is empty before showing a new passphrase
        app.output_frame.passphrase.set("")

        # Generate a passphrase
        self.generate_passphrase()
        print(self.passphrase)
        # If the word list was successfully opened, the list is populated, so go on to process the passphrase
        if len(self.word_list) > 0:
            self.process_passphrase()

        # display the passphrase, and remove the trailing blank space
        app.output_frame.passphrase_entry.insert(END, (self.passphrase.rstrip()))

    def generate_passphrase(self):
        """Get the passphrase from the Diceware word list."""

        self.word_list = []
        self.passphrase = ""
        # crypt_gen = Diceware()

        i = 1
        while i <= int(app.input_frame.word_count.get()):
            self.crypt_gen.dice_roll()
            try:
                self.word_list.append(self.crypt_gen.word_lookup())
                i += 1
            except FileNotFoundError:
                break

        for word in self.word_list:
            # add the processed word to the passphrase, and add a blank space between the words
            self.passphrase += (word + " ")

    def process_passphrase(self):
        """Process the word list"""

        # if we want to insert some random number substitution or capitalisation
        if app.input_frame.opt_allow_num.get() != 0:
            while not self.substitution_check() and not self.number_check():  # if False, generate new passphrase
                self.generate_passphrase()
            while not self.number_check():  # Guarantee at least one number in passphrase
                self.number_replacement()

        # guarantee at lease one capital letter in passphrase
        if app.input_frame.opt_allow_caps.get() != 0:
            while not self.letter_check():  # If ensures that the passphrase contains letter in order to capitalise them
                self.generate_passphrase()
            while not self.capital_check():
                self.capitalise()

    def number_replacement(self):
        """
        Replace a letter for a number if the letter exist in the dictionary of replacement letters (a, b, e, g, i, o, s,
        t, z) and then applies a 25% chance to replace the letter with the number in the dictionary.
        """
        modify_word = ""
        for letter in self.passphrase:
            # only perform number substitution if the letter is in the dictionary and a random number is 1
            if letter in LETTER_TO_NUMBER and (SystemRandom().randrange(0, 4) == 1):
                modify_word += LETTER_TO_NUMBER[letter]
            else:
                modify_word += letter

        self.passphrase = modify_word

    def capitalise(self):
        """
        Capitalise a letter. There is a 25% chance for a letter to be capitalised.
        """
        modify_word = ""
        for letter in self.passphrase:
            # only perform capitalisation if the letter is in the dictionary and a random number is 1
            if SystemRandom().randrange(0, 4) == 1:
                modify_word += letter.upper()
            else:
                modify_word += letter

        self.passphrase = modify_word

    def substitution_check(self):
        """
        Check if the passphrase contains any letters that can be substituted (e.g., contains only punctuation)
        """
        return any(char in LETTER_TO_NUMBER for char in self.passphrase)

    def number_check(self):
        """
        Check if the passphrase contains any numbers
        """
        return any(char.isdigit() for char in self.passphrase)

    def capital_check(self):
        """
        Check if the passphrase contains any capital letters
        """
        return any(char.isupper() for char in self.passphrase)

    def letter_check(self):
        """
        Check if the passphrase contains any letters
        """
        return any(char in string.ascii_letters for char in self.passphrase)

    def puctuation_check(self):
        """
        Check if the passphrase contains any punctuation. Not currently used. Possibly implemented in later versions.
        """
        return any(char in string.punctuation for char in self.passphrase)


def right_click(entry):
    """Right click context menu for passphrase entry box
    """

    try:
        # For added ease, let's select all and copy with one click
        def copy(entry, apnd=0):
            entry.widget.event_generate('<Control-a>')
            entry.widget.event_generate('<Control-c>')

        # Copy only the selected text
        def selected_copy(entry, apnd=0):
            entry.widget.event_generate('<Control-c>')

        entry.widget.focus()

        rmenu = Menu(None, tearoff=0, takefocus=0)
        rmenu.add_command(label="Select All & Copy", command=lambda entry=entry: copy(entry))
        rmenu.add_command(label="Copy Selected to Clipboard", command=lambda entry=entry: selected_copy(entry))
        rmenu.tk_popup(entry.x_root + 40, entry.y_root + 10, entry="0")

    except TclError:
        pass


if __name__ == '__main__':
    # Main Window
    #
    root = Tk()
    root.title(TITLE + " " + VERSION)

    app = App(root)
    app.pack(side="top", fill="both")

    # Bind the right-click menu to the passphrase entry widget
    app.output_frame.passphrase_entry.bind('<Button-3>', right_click, add='')

    root.mainloop()
