# -*- coding: utf-8 -*-
"""
threaded_test.py

Tests the tkit.ThreadedApp class.
Author: Garin Wally; Oct 2017
License: MIT
"""

import time
import Tkinter as tk
import tkit


def main_func(self):
    label = tk.Label(self, text="Thread test")
    label.pack()
    self.update()
    time.sleep(2)

    for i in range(11):
        time.sleep(0.5)
        if i == 0:
            label.config(text="Starting...")
            self.update()
            time.sleep(1.5)
        if i == 10:
            label.config(text="Complete!")
        else:
            label.config(text=i)
        self.update()
    return


if __name__ == "__main__":
    app = tkit.ThreadedApp("A Threaded App")
    menubar = tkit.Menubar(app)
    menubar.add_menu("File")
    menubar.add_action("File", "Close", menubar.quit)
    menubar.add_menu("Tools")
    menubar.add_action("Tools", "Import", None)
    menubar.add_action("Tools", "Export", None)
    menubar.add_submenu("Tools", "Models")
    menubar.menus["Tools"].items["Models"].add_action("Population Model", None)
    menubar.add_menu("Help")
    menubar.add_action(
        "Help", "About", tkit.Popup("About", __doc__).show_info)

    app.add_widget(menubar)
    app.add_button("Start", app.run)
    app.add_button("Close", app.close)

    app.set_main(main_func)
    
    app.mainloop()
