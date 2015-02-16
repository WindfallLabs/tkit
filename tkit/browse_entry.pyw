import Tkinter as tk
import ttk, tkFileDialog

import apptools

from os import path
from os import getcwd


# Browse Field (finalizing)
class BrowseEntry(ttk.LabelFrame):
    """ Pre-built open-file dialog/entry """
    def __init__(self, root):
        # Input Frame
        self.Container = ttk.LabelFrame(root, text=' Select File')
        self.Container.pack(side='top', anchor='n', fill='x', expand='yes', padx=5, pady=5)
        
        # Browse Entry
        self.fileVar = tk.StringVar()
        self.fileEntry = ttk.Entry(self.Container, width=30)
        self.fileEntry.pack(side='left', anchor='nw', fill='x', expand='yes', padx=5, pady=5)
        
        # Implement copy/paste
        # Browse Button
        try:
            #gif = getcwd() + '/Icons/openfolder.gif'
            gif = r"C:\Workspace\PROJECTS\Tkit\Tkit\Icons\openfolder.gif"
            #self.opengif = tk.PhotoImage(file=r'Icons\openfolder.gif')
            self.opengif = tk.PhotoImage(file=gif)
            browseBut = ttk.Button(self.Container, command=self.Browse_file)
            browseBut.config(image = self.opengif)
        except:
            browseBut = ttk.Button(self.Container, text=' ... ', command=self.Browse_file)
            
        browseBut.pack(side='right', anchor='ne', padx=5, pady=5)
        #browseBut.config(image = self.opengif)
        
    
    def set_BrowseFiletypes(self, default_ext, types_tupelist):
#        self.FILEOPENOPTIONS = dict(defaultextension='.bin',
#                                    filetypes=[('All files','*.*'), ('Bin file','*.bin')])
        self.FILEOPENOPTIONS = dict(defaultextention=default_ext, filetypes=types_tupelist)
        
    def Browse_file(self):
        # Get file
        tk.Tk().withdraw()
        try:
            browse_file = tkFileDialog.askopenfilenames(**self.FILEOPENOPTIONS)
        except:
            browse_file = tkFileDialog.askopenfilenames()
        parent_dir = path.dirname(browse_file)
        self.fileEntry.delete(0, "end")
        self.fileEntry.insert(0, browse_file)
        self.fileVar.set(browse_file)
        return browse_file, parent_dir
        
    def get_fileVar(self):
        return self.fileVar.get()

# Sources:
# https://stackoverflow.com/questions/4297949/image-on-a-button

#===================================================================
# End of BrowseField Module
#===================================================================
# Test Application code:

class _App(tk.Frame):
    """ Testing GUI """
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        BrowseEntry(self)


if __name__ == '__main__':
    apptools.thread_GUI(_App)
