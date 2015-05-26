########################################################################################################################
# Author: David Cartwright
# Date: 01 May 2015
# Version: 0.1
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
# 0.1 29/01/2015 - Initial Release
########################################################################################################################

# Import Modules
from tkinter import *
from tkinter import ttk
from diceware import Diceware

# Software Information
VERSION = "0.1"
TITLE = "Diceware Passphrase Generator"


class InputFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        self.input_frm = ttk.LabelFrame(self, text="Configuration: ")
        self.input_frm.pack(side=TOP, fill=BOTH)

        ttk.Label(self.input_frm, text="Number of Words: ").pack(side=LEFT)

        # Create a spinbox, with a range of 1 to 10, and then set the default to 5
        self.num_of_words = StringVar()
        self.word_count = Spinbox(self.input_frm, from_=1, to=10, textvariable=self.num_of_words)
        self.word_count.pack(side=LEFT, padx=5, pady=5)
        self.word_count.delete(0, END)
        self.word_count.insert(0, 5)

        # Create the 'Generate' button and give it focus
        self.generate_btn = ttk.Button(self.input_frm, text="Generate", command=get_passphrase)
        self.generate_btn.pack(side=RIGHT, padx=5, pady=5)
        self.generate_btn.focus_set()

        self.generate_btn.bind('<Return>', get_passphrase)

        # Add some padding
        for child in self.input_frm.winfo_children():
            child.pack_configure(padx=5, pady=5)


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

        # Add some padding
        for child in self.output_frm.winfo_children():
            child.pack_configure(padx=5, pady=5)


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


def get_passphrase(event=None):
    """Get the passphrase from the Diceware word list."""

    word_list = list()
    crypt_gen = Diceware()

    i = 1
    while i <= int(app.input_frame.word_count.get()):
        crypt_gen.dice_roll()
        try:
            word_list.append(crypt_gen.word_lookup())
            i += 1
        except:
            break

    if word_list:
        # Ensure that the passphrase box is empty before showing a new passphrase
        app.output_frame.passphrase.set("")
        for word in word_list:
            app.output_frame.passphrase_entry.insert(END, (word + " "))

        # Since the while loop adds a space after each word, we want to remove the last space that gets added
        app.output_frame.passphrase_entry.delete(len(app.output_frame.passphrase_entry.get()) - 1, END)


def right_click(entry):
    """Right click context menu for passphrase entry box
    """

    try:
        # For added ease, let's select all and copy with one click
        def copy(entry, apnd=0):
            entry.widget.event_generate('<Control-a>')
            entry.widget.event_generate('<Control-c>')

        entry.widget.focus()

        rmenu = Menu(None, tearoff=0, takefocus=0)
        rmenu.add_command(label="Select All & Copy", command=lambda entry=entry: copy(entry))
        rmenu.tk_popup(entry.x_root+40, entry.y_root+10, entry="0")

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
