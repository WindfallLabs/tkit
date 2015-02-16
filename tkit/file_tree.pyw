""" A tk list-tree """
# Dev Notes:
__status__ = 'pre-alpha'
#   Implement file browser functionality
#   Test
#

# Imports
import Tkinter as tk
import ttk

import apptools


# Consider "ListTree" as name
class FileTree(ttk.LabelFrame):
    """ Allows user to easily manipulate columns of data """
    def __init__(self, root):
        self.container = ttk.LabelFrame(root, text=' Tabel Label ')
        self.container.pack(side='top', anchor='n', fill='x', expand='yes', padx=5, pady=5)
        self.headers = "Col 1"
        self.build_tree()
        self.add_controls()
        
    def build_tree(self):
        tree = ttk.Treeview(self.container, show="headings",height=5)
        tree["columns"] = "single"
        tree.column("single", width=200)
        tree.heading("single", text="Input Files")
        tree.pack(fill='x')

    def add_controls(self):
        """ Controls for manipulating Tree contents """
        # Add button - adds table contents
        self.AddBut = ttk.Button(self.container, text='Add')
        self.AddBut.pack(side='left')
        # Remove button - removes selected table contents
        self.RemoveBut = ttk.Button(self.container, text='Remove')
        self.RemoveBut.pack(side='right')
   

#===================================================================
# End of file_tree Module
#===================================================================
# Test Application code:

class _App(tk.Frame):
    """ Testing GUI """
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        FileTree(self)


if __name__ == '__main__':
    apptools.thread_GUI(_App)
