# -*- coding: utf-8 -*-
""" Tkit Testing App """

# Imports
import Tkinter as tk
import ttk

import apptools

from browse_entry import *
from file_tree import *
from radiobox import *
from statusbar import *
from menubar import *


# Testing GUI
class App(tk.Frame):
    """ Testing GUI """
    def __init__(self, root):
        """ Parent window properties """
        tk.Frame.__init__(self, root)
        self.root = root

        self.root.title('Tkit Import Test App')
        #self.root.geometry('300x300')
        resize = True
        if resize is False:
            self.root.resizable(0, 0)
        self.root.lift()
        self.root.focus_force()
        self.root.deiconify()

        """ Widgets """

        # Menubar
        self.menu = Menubar(self.root)
        self.root.configure(menu=self.menu)

        # Browse Field
        self.browse_ent = BrowseFile(self)

        self.browse_dir = BrowseDir(self)

        # Print selected browse fields
        self.print_but = ttk.Button(self, text=' Test print ',
                                    command=self.print_dir)
        self.print_but.pack()

        # Status Bar
        self.Ok_but = ttk.Button(self, text=' Test Status ',
                                 command=self.call_main)

        self.statusbar = Statusbar(self, self.Ok_but)

        # Ok button
        self.Ok_but.pack(side='right', anchor='se', padx=5, pady=5)

        # Radiobox
        self.radiobox = Radiobox(self, 'int', ' Wait Time ',
                                 'right', 'nw', 'both', 1)
        self.radiobox.add_button('Five', 5)
        self.radiobox.add_button('Ten', 10)
        self.radiobox.add_button('Fifteen', 15)

        # FileTree
        self.filetree = FileTree(self)

        """ Bindings """

        self.root.bind('<Return>', self.call_main)
        self.root.bind('<Escape>', self.close)

    """ Window Methods """

    def close(self, event=None):
        self.root.destroy()

    """ Main Method(s) """

    def print_dir(self):
        print self.browse_dir.get_value()
        print self.browse_ent.get_value()

    def call_main(self, event=None):
        """Threadifies Main() and passes parameters to it."""
        self.main_thread = apptools.ThreadedClient(
            "Main", lambda: self.Main(self.radiobox.get_selected()))
        self.main_thread.start()

    def Main(self, t):
        """Emulates process."""
        self.statusbar.start()
        sleep(t)
        self.statusbar.stop()

if __name__ == '__main__':
    apptools.thread_GUI(App)
