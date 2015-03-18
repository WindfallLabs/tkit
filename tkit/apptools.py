""" Provides reusable app dev code """

# Imports
import Tkinter as tk
import threading
import logging


def build_GUI(App_class):
    root = tk.Tk()
    App_class(root).pack(fill='both', expand='yes')
    root.mainloop()

def thread_GUI(App_class):
    GUI = ThreadedClient("GUI", lambda: build_GUI(App_class))
    GUI.start()
    GUI.join()

class ThreadedClient(threading.Thread):
    def __init__(self, name, process):
        """Subclass of thread allows for easier thread creation."""
        threading.Thread.__init__(self)
        self.name = name
        self.process = process
        
    def run(self):
        """Runs at thread start."""
        logging.debug("{0} thread started".format(self.name))
        self.process()
        logging.debug("{0} thread terminated".format(self.name))
