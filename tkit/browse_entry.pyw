""" A file browser-entry box """
# Dev Notes:
__status__ = 'alpha'
#   Implement copy/paste functionality -- import it from elsewhere
#

# Imports
import Tkinter as tk
import ttk
import tkFileDialog
from os import path, getcwd

import apptools


class BrowseEntry(ttk.LabelFrame):
    """ Pre-built open-file dialog/entry """
    def __init__(self, root):
        self.root = root
        # Input Frame
        self.Container = ttk.LabelFrame(root, text=" Select File ")
        self.Container.pack(side='top', anchor='n', fill='x',
                            expand='yes', padx=5, pady=5)

        # Default filetypes
        self.FILEOPENOPTIONS = dict(defaultextension='*.*',
                  filetypes=[('All files','*.*')])

        # Browse Entry
        self.fileVar = tk.StringVar()
        self.fileEntry = ttk.Entry(self.Container, width=30)
        self.fileEntry.pack(side='left', anchor='nw', fill='x',
                            expand='yes', padx=5, pady=5)
        
        # Copy/paste
        
        # Browse Button
        try:
            gif = r"C:\Workspace\PROJECTS\Tkit\Tkit\Icons\openfolder.gif"
            self.opengif = tk.PhotoImage(file=gif)
            self.browseBut = ttk.Button(self.Container,
                                   command=self.browse)
            self.browseBut.config(image = self.opengif)
        except:
            self.browseBut = ttk.Button(self.Container,
                                   text=" ... ",
                                   command=self.browse)
        self.browseBut.pack(side='right', anchor='ne', padx=5, pady=5)
    
    def set_filetypes(self, default_ext, types_tupelist):
        self.FILEOPENOPTIONS = None
        self.FILEOPENOPTIONS = dict(defaultextension=default_ext,
                                    filetypes=types_tupelist)
        
    def browse(self):
        """ Opens file browser and places selected file in entry """
        browse_file = tkFileDialog.askopenfilenames(parent=self.root,
                                                        **self.FILEOPENOPTIONS)

        # Place in entry box
        parent_dir = path.dirname(browse_file)
        self.fileEntry.delete(0, 'end')
        self.fileEntry.insert(0, browse_file)
        self.fileVar.set(browse_file)
        return browse_file, parent_dir
        
    def get_fileVar(self):
        return self.fileVar.get()

# Sources:
# https://stackoverflow.com/questions/4297949/image-on-a-button
# https://stackoverflow.com/questions/11352278/default-file-type-in-tkfiledialogs-askopenfilename-method

#===================================================================
# End of browse_entry Module
#===================================================================
# Test Application code:

class _App(tk.Frame):
    """ Testing GUI """
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.browse_ent = BrowseEntry(self)
        
        self.browse_ent.set_filetypes('.py',
                                      [('Python', '.pyw'),
                                       ('Python', '.py')])


if __name__ == '__main__':
    apptools.thread_GUI(_App)
