# -*- coding: utf-8 -*-
"""
threaded_test.py

Tests the tkit.ThreadedApp class.
Author: Garin Wally; Oct 2017
License: MIT
"""

from time import sleep
import Tkinter as tk
import ttk
import tkit


@tkit.threaded_gui
class TestApp(tk.Frame):
    """ Testing GUI """
    def __init__(self, root):
        """ Parent window properties """
        tk.Frame.__init__(self, root)
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.title('Tkit Import Test App')
        resize = True
        if resize is False:
            self.root.resizable(0, 0)
        self.root.lift()
        self.root.focus_force()
        self.root.deiconify()

        """ Widgets """

        # Menubar
        self.menubar = tkit.Menubar(self)
        self.menubar.add_menu("File")
        self.menubar.menus["File"].add_action("Close", self.quit)
        self.menubar.add_menu("Edit")
        self.menubar.menus["Edit"].add_action("None", None)
        self.menubar.add_menu("Data")
        self.menubar.add_menu("Tools")
        self.menubar.menus["Tools"].add_action("Import", None)
        self.menubar.menus["Tools"].add_action("Export", None)
        self.menubar.add_submenu("Tools", "Models")
        self.menubar.menus["Tools"].items["Models"].add_action(
            "Building Permits", None)
        self.menubar.add_menu("View")
        self.menubar.menus["View"].add_action("Console", None)
        self.menubar.add_menu("Help")
        self.menubar.menus["Help"].add_action(
            "About", tkit.Popup("About", "Stuff").show_info)
        self.menubar.set_parent(self.root)

        # Browse Field
        self.browse_ent = tkit.BrowseFile(self)

        self.browse_dir = tkit.BrowseDir(self)

        # Print selected browse fields
        self.print_but = ttk.Button(self, text=' Test print ',
                                    command=self.print_dir)
        self.print_but.pack()

        # Status Bar
        self.Ok_but = ttk.Button(self, text=' Test Status ',
                                 command=self.call_main)

        self.statusbar = tkit.Statusbar(self, self.Ok_but)

        # Ok button
        self.Ok_but.pack(side='right', anchor='se', padx=5, pady=5)

        # Radiobox
        self.radiobox = tkit.Radiobox(self, 'int', ' Wait Time ',
                                 'right', 'nw', 'both', 1)
        self.radiobox.add_button('Five', 5)
        self.radiobox.add_button('Ten', 10)
        self.radiobox.add_button('Fifteen', 15)

        # FileTree
        self.filetree = tkit.FileTree(self)

        """ Bindings """

        self.root.bind('<Return>', self.call_main)
        self.root.bind('<Escape>', self.close)

    """ Window Methods """

    def close(self, event=None):
        self.root.destroy()
        self.master.quit()
        return

    """ Main Method(s) """

    def print_dir(self):
        print self.browse_dir.get()
        print self.browse_ent.get()

    def call_main(self, event=None):
        """Threadifies Main() and passes parameters to it."""
        self.main_thread = tkit.ThreadedClient(
            "Main", lambda: self.Main(self.radiobox.get()))
        self.main_thread.start()

    def Main(self, t):
        """Emulates process."""
        self.statusbar.start()
        sleep(t)
        self.statusbar.stop()
