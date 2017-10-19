# -*- coding: utf-8 -*-
"""
app_test.py

Tests the tkit.App class.
Author: Garin Wally; Oct 2017
License: MIT
"""

import tkit


if __name__ == "__main__":
    # Create app
    test_app = tkit.App("Test App", 250, 100)
    # Create and customize menubar
    menubar = tkit.Menubar()
    menubar.add_menu("File")
    #test_menubar.menus["File"].add_action("Test", app.mainloop)
    menubar.menus["File"].add_action("Close", test_app.close)
    menubar.add_menu("Help")
    menubar.menus["Help"].add_action(
        "About", tkit.Popup("About", "This program ...").show_info)
    # Add menubar to app
    test_app.add_widget(menubar)

    test_app.add_widget(tkit.BrowseFile())
    # Run it
    test_app.add_button("OK", test_app.cmd_collect_values)
    test_app.mainloop()
