""" A tk list-tree """
# Dev Notes:
__status__ = 'pre-alpha'
#   Implement file browser functionality
#   Test
#

# Imports
import Tkinter as tk
import ttk
import tkFileDialog

import apptools


# Consider "ListTree" as name
class FileTree(ttk.LabelFrame):
    """ Allows user to easily manipulate columns of data """
    def __init__(self, root):
        self.root = root
        
        # Container
        self.container = ttk.LabelFrame(root, text=' Tabel Label ')
        self.container.pack(side='top', anchor='n', fill='x',
                            expand='yes', padx=5, pady=5)
        self.headers = "Col 1"

        # Tree
        tree = ttk.Treeview(self.container, show="headings",height=5)
        tree["columns"] = "single"
        tree.column("single", width=200)
        tree.heading("single", text="Input Files")
        tree.pack(fill='x')

        # Add button - adds table contents
        self.Add_but = ttk.Button(self.container, text='Add')
        self.Add_but.pack(side='left')
        # Remove button - removes selected table contents
        self.Remove_but = ttk.Button(self.container, text='Remove')
        self.Remove_but.pack(side='right')
        
        # Default filetypes
        self.FILEOPENOPTIONS = dict(defaultextension='*.*',
                  filetypes=[('All files','*.*')])
        
    def set_filetypes(self, default_ext, types_tupelist):
        self.FILEOPENOPTIONS = None
        self.FILEOPENOPTIONS = dict(defaultextension=default_ext,
                                    filetypes=types_tupelist)
        
    def add_file(self):
        """ Opens file browser and places selected file(s) in tree """
        browse_file = tkFileDialog.askopenfilenames(parent=self.root,
                                                        **self.FILEOPENOPTIONS)
   

#===================================================================
# End of file_tree Module
#===================================================================
# Test Application code:

class _App(tk.Frame):
    """ Testing GUI """
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.filetree = FileTree(self)


if __name__ == '__main__':
    apptools.thread_GUI(_App)
