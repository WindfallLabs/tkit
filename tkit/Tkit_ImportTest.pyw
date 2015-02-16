import threading
import Queue
import Tkinter as tk
import ttk

import AppTools

from BrowseEntry import *
from FileTree import *
from Radiobox import *
from Statusbar import *


# Testing GUI
class App(tk.Frame):
    """ Testing GUI """
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        
        """ Window Properties """
        self.root.title('Tkit Import Test App')
        #self.root.geometry('300x300')
        resize = True
        if resize == False:
            self.root.resizable(0,0)
        self.root.lift()
        self.root.focus_force()
        self.root.deiconify()

        """ Widgets """
        
        # Browse Field
        BrowseEntry(self)

        self.Ok_but = ttk.Button(self, text=' Test Status ', command=self.call_main)
        
        # Status Bar
        self.statusbar = Statusbar(self, self.Ok_but)

        self.Ok_but.pack(side='right', anchor = 'se', padx=5, pady=5)
        self.radiobox = Radiobox(self, 'int', ' Wait Time ',
                                 'right', 'nw', 'both', 1)
        self.radiobox.add_button('Five', 5)
        self.radiobox.add_button('Fifteen', 15)

        
        
        FileTree(self)

        
    def call_main(self, *event):
        """ Threadifies Main() and passes parameters to it """
        self.main_thread = AppTools.ThreadedClient("Main",
                                          lambda: self.Main(self.radiobox.get_selected()))
        self.main_thread.start()

    def Main(self, t):
        """ emulates process """
        self.statusbar.start()
        sleep(t)
        self.statusbar.stop()

if __name__ == '__main__':
    AppTools.thread_GUI(App)
