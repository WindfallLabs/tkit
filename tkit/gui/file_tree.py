# -*- coding: utf-8 -*-
""" A tk list-tree """

# Imports
import Tkinter as tk
import ttk
import tkFileDialog
# from os import path

import apptools


# Consider "ListTree" as name
class FileTree(ttk.LabelFrame):
    """Allows user to easily manipulate columns of data."""
    def __init__(self, root):
        self.root = root

        # Vars
        self.fileList = []

        # Container
        self.container = ttk.LabelFrame(root, text=' Tabel Label ')
        self.container.pack(side='top', anchor='n', fill='x',
                            expand='yes', padx=5, pady=5)
        self.headers = "Col 1"

        # Tree
        self.tree = ttk.Treeview(self.container, show="headings", height=5)
        self.tree["columns"] = "single"
        self.tree.column("single", width=200)
        self.tree.heading("single", text="Input Files")
        self.tree.pack(fill='x')

        # Duplicate Warning
        self.warning = ttk.Label(self.container,
                                 text="Warning:\nDuplicates will be removed")

        # Add button - adds table contents
        self.Add_but = ttk.Button(self.container, text='Add',
                                  command=self.add_file)
        self.Add_but.pack(side='left')

        # Remove button - removes selected table contents
        self.Remove_but = ttk.Button(self.container, text='Remove',
                                     command=self.rm_file)
        self.Remove_but.pack(side='right')

        # Default filetypes
        self.FILEOPENOPTIONS = dict(defaultextension='*.*',
                                    filetypes=[('All files', '*.*')])

    def set_filetypes(self, default_ext, types_tupelist):
        self.FILEOPENOPTIONS = None
        self.FILEOPENOPTIONS = dict(defaultextension=default_ext,
                                    filetypes=types_tupelist)

    def add_file(self):
        """Opens file browser and places selected file(s) in tree."""
        new_file = tkFileDialog.askopenfilenames(parent=self.root,
                                                 **self.FILEOPENOPTIONS)
        print(new_file)
        for f in new_file:
            self.fileList.append(f)
            self.tree.insert("", 'end', values=f)

        if len(self.fileList) != len(set(self.fileList)):
            self.warning.pack(side='bottom')

    def rm_file(self):
        """Removes selected file from tree."""
        current_val = self.tree.item(self.tree.focus())['values'][0]
        self.tree.delete(self.tree.focus())
        self.fileList.remove(current_val)
        # Attempts to remove duplicate warning
        if len(self.fileList) == len(set(self.fileList)):
            self.warning.pack_forget()

    def get_list(self):
        """Returns selected list of selected files."""
        self.fileList = list(set(self.fileList))
        print self.fileList
        return self.fileList


# =============================================================================
# End of file_tree Module
# =============================================================================
# Test Application code:


class _App(tk.Frame):
    """Testing GUI"""
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.filetree = FileTree(self)

        self.Ok_but = ttk.Button(text=" Pass ",
                                 command=self.filetree.get_list)
        self.Ok_but.pack(side='bottom')


if __name__ == '__main__':
    apptools.thread_GUI(_App)
