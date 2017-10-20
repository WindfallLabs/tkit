# -*- coding: utf-8 -*-
"""
threaded_test.py

Tests the tkit.ThreadedApp class.
Author: Garin Wally; Oct 2017
License: MIT
"""

import time
import itertools
import threading
import Tkinter as tk

import tkit


STOP = threading.Event()


def sleep():
    """A worker simulating a long process."""
    print("Sleeping...")
    time.sleep(8)
    print("Done sleeping")
    STOP.set()
    spinner.stop()
    return


def do_stuff():
    """A worker simulating a short process."""
    print("Stuff done.")
    

def w_loop():
    """A worker simulating a looping process."""
    while not STOP.is_set():
        print("Still looping...")
        time.sleep(.75)


def some_process(self):
    """This method-like function will become a method of the app class."""
    # Set the label
    label = tk.Label(self, text="Testing...")
    label.pack()
    self.update()

    # Starts these functions and moves on
    tkit.thread_tasks([w_loop, sleep, do_stuff])

    self.start_spinner() # Hangs here until sleep sets the STOP event
    label.config(text="Done.")
    self.update()
    return


if __name__ == "__main__":
    app = tkit.App("A Threaded Example")
    
    menubar = tkit.Menubar(app)
    menubar.add_menu("File")
    menubar.add_action("File", "Close", menubar.quit)
    menubar.add_menu("Help")
    menubar.add_action(
        "Help", "About", tkit.Popup("About", __doc__).show_info)

    spinner = tkit.Elipse(app, word="")

    app.add_command("some_process", some_process)

    app.add_button("Start", app.some_process)
    app.add_button("Close", app.close)
    
    app.mainloop()
