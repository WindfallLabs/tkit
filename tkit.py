# -*- coding: utf-8 -*-
"""tkit.py -- Tkinter Tool Kit

This module provides a light, object-oriented API for rapid GUI design with
Tkinter.

Author: Garin Wally; Feb 2015
"""

# Imports
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

import os
import re
import ttk
import tkMessageBox
import tkFileDialog
import threading
import logging
from collections import OrderedDict
from time import sleep

# Logging output
logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s')

# Location of module
_DIR = os.path.dirname(__file__)
# Open folder icon
OPENFOLDER = os.path.join(_DIR, "icons/openfolder.gif").replace("\\", "/")


def NULL_ACTION():
    """Function to replace calling None."""
    pass


def _clean_name(name):
    return re.sub("[\W]", "", name.lower().replace(" ", "_"))


# ==============================================================================
# THREADING

def build_gui(app):
    root = tk.Tk()
    app(root).pack(fill='both', expand='yes')
    root.mainloop()


def threaded_gui(app):  # TODO: not start immediately...
    gui = ThreadedClient("GUI", lambda: build_gui(app))
    gui.start()
    gui.join()


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


# ==============================================================================
# APP WINDOWS

class SimpleApp(tk.Tk):
    def __init__(self, title="", width=400, height=200):
        tk.Tk.__init__(self)

        # Parent window properties
        self.geometry("{width}x{height}".format(width=width, height=height))
        self.title(title)
        self._startup()

        # All child widgets should have parent/root set to the app
        # Widgets objects are referenced in the widgets dict by name
        self.widgets = {}
        self.input_values = {}

    def _startup(self):
        # Force to top when opened
        self.attributes("-topmost", True)
        self.attributes("-topmost", False)
        # Activate/focus on window
        self.focus_force()
        # Set window close (X) handler
        self.protocol("WM_DELETE_WINDOW", self.close)

    def add_widget(self, name, widget):
        widget.set_parent(self)
        self.widgets[_clean_name(name)] = widget
        return

    def close(self):
        # Close the window
        self.destroy()
        # End the process
        self.quit()

    def set_topmost(self, on_top=True):
        self.attributes("-topmost", on_top)
        return


class App(SimpleApp):
    def __init__(self, title="", width=400, height=200):
        SimpleApp.__init__(self)
        self._startup()

    def add_button(self, label, action, **kwargs):
        button = ttk.Button(self, text=label, command=action)
        button.pack(kwargs)
        name = _clean_name(label)
        self.widgets[name + "_button"] = button
        return

    def add_text_input(self, label, length=20):
        ttk.Label(text="{} ".format(label)).pack(padx=10, pady=0)
        text_box = ttk.Entry(self, width=length)
        text_box.pack(padx=10, pady=10)
        name = _clean_name(label)
        self.widgets[name + "_textbox"] = text_box
        return

    def cmd_collect_values(self):
        for name, widget in self.widgets.items():
            try:
                input_val = widget.get()
                print(input_val)
                self.input_values[name] = input_val
            except (AttributeError, tk.TclError):
                pass

    def cmd_collect_quit(self):
        self.cmd_collect_values()
        self.close()
        return


# TODO:
'''
@threaded_gui
class ThreadedApp(App):
    def __init__(self):
        App.__init__(self, "Name")
'''


class Popup(SimpleApp):
    """Wrapper object for tkMessageBox."""
    def __init__(self, title="", message=""):
        """A popup window that is displayed using .show_ methods."""
        SimpleApp.__init__(self, title)
        # Hide the root window
        self.withdraw()
        self.name = title
        self.message = message
        self.input = None

    def show_ok_cancel(self):
        """Display a popup with 'OK' and 'Cancel'. Returns True or False."""
        self.input = tkMessageBox.askokcancel(self.name, self.message)
        return

    def show_yes_no(self, cancel=False):
        """Display a popup with 'Yes', 'No', and optionally 'Cancel'.
        Returns True, False, or None."""
        if cancel:
            self.input = tkMessageBox.askyesnocancel(self.name, self.message)
            return
        self.input = tkMessageBox.askyesno(self.name, self.message)
        return

    def show_info(self):
        """Display an info popup with 'OK' button. Returns 'ok'."""
        self.input = tkMessageBox.showinfo(self.name, self.message)
        return

    def show_warn(self):
        """Display a warning popup with 'OK' button. Returns 'ok'."""
        self.input = tkMessageBox.showwarning(self.name, self.message)
        return

    def show_error(self):
        """Display an error popup with 'OK' button. Returns 'ok'."""
        self.input = tkMessageBox.showerror(self.name, self.message)
        return


class FileDialog(App):
    """Wrapper object for tkFileDialog."""
    pass  # TODO: wrap the file dialog stuff found in FileTree and Browse...


# =============================================================================
# MENUBAR

class Menubar(tk.Menu):
    def __init__(self, root):
        tk.Menu.__init__(self, root=None)
        self.root = root
        self.name = "menubar"
        # Set the underlying app's menu to self (this Menubar object)
        try:
            self.root.config(menu=self)
        except:
            pass
        self.menus = OrderedDict()

    def set_parent(self, parent):
        self.root = parent
        self.root.config(menu=self)
        return

    def quit(self):
        self.root.destroy()

    def add_menu(self, name, underline=0):
        menu = Menu(self)
        self.add_cascade(label=name, underline=underline, menu=menu)
        self.menus[name] = menu
        return

    '''
    def add_action(self, menu, name, action):
        """Adds an action to a specified menu."""
        self.menus[menu].add_action(name, action)
        return
    '''

    def add_submenu(self, menu, name):
        """Adds an action to a specified menu."""
        self.menus[menu].add_submenu(name)
        return


class Menu(tk.Menu):
    def __init__(self, root):
        tk.Menu.__init__(self, root, tearoff=False)
        self.root = root
        self.items = OrderedDict()

    def add_action(self, name, action):
        """Adds an action to the current menu."""
        if not action:
            action = NULL_ACTION
        self.items.update({name: action})
        self.add_command(label=name, command=action)
        return

    def add_submenu(self, name, underline=0):
        """Adds an action to the current menu."""
        menu = Menu(self)
        self.add_cascade(label=name, underline=underline, menu=menu)
        self.items[name] = menu
        return


'''
class App(tk.Tk):
    def __init__(self, title="", length=400):
        tk.Tk.__init__(self)
        self.title(title)

        menubar = Menubar(self)
        menubar.add_menu("File")
        menubar.add_action("File", "Close", menubar.quit)

        menubar.add_menu("Edit")
        menubar.add_action("Edit", "None", None)

        menubar.add_menu("Data")

        menubar.add_menu("Tools")
        menubar.add_action("Tools", "Import", None)
        menubar.add_action("Tools", "Export", None)
        menubar.add_submenu("Tools", "Models")
        menubar.menus["Tools"].items["Models"].add_action(
            "Building Permits", None)

        menubar.add_menu("View")
        menubar.add_action("View", "Console", None)

        menubar.add_menu("Help")
        menubar.add_action("Help", "About", None)

        # Widgets can't be called with self, so reference them here
        self.widgets = {
            "menu": menubar}

        self.geometry("{}x0".format(length))
'''
'''
if __name__ == "__main__":
    app = App("Garin")
    app.mainloop()
'''


# =============================================================================
# STATUSBAR

class Statusbar(tk.Frame):
    """Places status bar and label in frame."""
    def __init__(self, root, disable_button=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self.status_thread = ThreadedClient("Statusbar", self.start_bar)
        self.wait_event = threading.Event()
        self.root_but = disable_button

        # Status (label)
        self.labels = ["Ready", "Working...", "Done"]
        self.cur_status = 0

        # Statusbar container
        self.bar = ttk.Frame(root, relief='raised')

        self.bar.pack(side='bottom', anchor='s', fill='x',
                      expand='yes', padx=0, pady=0)

        # Status labels
        self.status_label = ttk.Label(self.bar, text=self.labels[0])
        self.status_label.pack(side='left', anchor='sw', padx=2, pady=5)

        # Progress bar
        self.progressbar = ttk.Progressbar(self.bar, orient='horizontal',
                                           length=200, mode='indeterminate')

        # Reset button
        self.reset_but = tk.Button(self.bar, text="Reset", command=self.reset)
        self.reset_but.config(relief='flat',
                              overrelief="groove",
                              height=0)

    def reset(self):
        """Resets the status bar."""
        self.root_but.config(state="enabled")
        self.progressbar.pack_forget()
        self.update_bar()
        self.status_thread = ThreadedClient("Statusbar", self.start_bar)
        self.wait_event = threading.Event()
        self.reset_but.pack_forget()

    def update_bar(self):
        """Changes status label and packs/unpacks progress bar."""
        self.cur_status += 1
        if self.cur_status > 2:
            self.cur_status = 0
        self.status_label.config(text=self.labels[self.cur_status])
        if self.cur_status == 1:
            self.progressbar.pack(side='right', expand='y',
                                  fill='x', padx=5, pady=2)
        elif self.cur_status == 2:
            self.reset_but.pack(side='right')
            # self.progressbar.pack_forget() # Issue here

    def start_bar(self):
        """Controls the bar."""
        self.root_but.config(state='disabled')
        self.progressbar.start(1)
        self.wait_event.wait()
        logging.debug("Status wait event done")
        self.progressbar.stop()
        logging.debug("Bar stopped")

    def start(self):
        """Starts the status thread."""
        self.update_bar()
        self.status_thread.start()

    def stop(self):
        """Stops the bar at the event flag."""
        self.wait_event.set()
        self.update_bar()


'''
class _App(tk.Frame):
    """Testing GUI"""
    def __init__(self, root):
        # Parent window properties
        tk.Frame.__init__(self, root)
        self.root = root
        self.root.title("Statusbar Testing App")
        self.root.geometry('160x100')

        """ Testing Variables """

        self.Main_val = 5

        """ Widgets """

        # OK Button runs Main() and sends parameters (from tk widgets)
        self.Ok_but = ttk.Button(text=" OK ",
                                 command=self.call_main)
        self.Ok_but.pack()

        # Imported StatusBar will be used as so
        self.statusbar = Statusbar(self, self.Ok_but)

        """ Bindings """

        # Allows user to press "Enter" instead of clicking the OK button
        self.root.bind('<Return>', self.call_main)

        # Allows user to press "Escape" instead of clicking the Close button
        self.root.bind('<Escape>', self.close)

    """ Window Methods """

    def close(self, event=None):
        self.root.destroy()

    """ Main Method(s) """

    def call_main(self, event=None):
        """Threadifies Main() and passes parameters to it."""
        self.main_thread = apptools.ThreadedClient(
            "Main", lambda: self.Main(self.Main_val))
        self.main_thread.start()

    def Main(self, t):
        """Emulates process."""
        logging.debug('Processing...')
        self.statusbar.start()
        sleep(t)
        logging.debug('Processing Complete')
        self.statusbar.stop()  # Should also hide/pack_forget the prog bar
'''
'''
if __name__ == '__main__':
    apptools.thread_GUI(_App)
'''


# =============================================================================
# RADIOBOX

class Radiobox(ttk.LabelFrame):
    """Allows user to easily place radio buttions into a labelframe."""
    def __init__(self, root, var_type, labelframe_text, box_side,
                 box_anchor, box_fill, box_expand, r_alignment='horizontal'):
        # Container
        self.Container = ttk.LabelFrame(root, text=labelframe_text)
        self.Container.pack(fill=box_fill, expand=box_expand, side=box_side,
                            anchor=box_anchor, padx=5, pady=5)

        # Default radiobutton value
        if var_type == "string" or var_type == "str":
            self.radio_value = tk.StringVar()
        else:
            self.radio_value = tk.IntVar()

        # Alignment method for radio buttons ('horizontal' or 'vertical')
        # What if the user wants a grid of radio buttons?
        # N x N or max_row / max_col?
        #  alignment_methods = {0: 'horizontal', 1: 'vertical'}
        self.button_alignment = r_alignment
        self.r_column = 0
        self.r_row = 0

    def add_button(self, radio_name, in_value):
        """Adds a new button to the radiobox."""
        rbutton = ttk.Radiobutton(self.Container, text=radio_name,
                                  value=in_value, variable=self.radio_value)
        rbutton.grid(column=self.r_column, row=self.r_row)
        if self.button_alignment == 'horizontal':
            self.r_column += 1
        else:
            self.r_row += 1

    def get(self):
        """Returns the value of the selected radiobutton."""
        return self.radio_value.get()

    def _print_selected(self):
        """For Testing"""
        print self.radio_value.get()


'''
class _App(tk.Frame):
    """Testing GUI"""
    def __init__(self, root):
        """ Parent window properties """
        tk.Frame.__init__(self, root)
        self.root = root
        self.root.title("Radiobox Test App")

        """ Widgets """

        self.radiobox = Radiobox(self, 'str', " Radios ", 'top',
                                 'nw', 'both', 'yes', 1)
        self.radiobox.add_button('Option 1', 'One')
        self.radiobox.add_button('Option 2', 'Two')
        self.radiobox.add_button('Option 3', 'Three')

        self.Ok_but = ttk.Button(text=" Print ",
                                 command=self.radiobox._print_selected)
        self.Ok_but.pack(side='bottom')
'''
'''
if __name__ == '__main__':
    apptools.thread_GUI(_App)
'''


# =============================================================================
# FILETREE

class FileTree(ttk.LabelFrame):  # TODO: Consider "ListTree" as name
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
        print(self.fileList)
        return self.fileList


'''
class _App(tk.Frame):
    """Testing GUI"""
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.filetree = FileTree(self)

        self.Ok_but = ttk.Button(text=" Pass ",
                                 command=self.filetree.get_list)
        self.Ok_but.pack(side='bottom')
'''
'''
if __name__ == '__main__':
    apptools.thread_GUI(_App)
'''


# =============================================================================
# BROWSEFILE

class BrowseFile(ttk.LabelFrame):
    """Select a file(s) and add it to an entrybox"""
    def __init__(self, root=None):
        self.root = root
        # Input Frame
        self.Container = ttk.LabelFrame(root, text=" Select File ")
        self.Container.pack(side='top', anchor='n', fill='x',
                            expand='yes', padx=5, pady=5)

        # Default filetypes
        self.FILEOPENOPTIONS = dict(defaultextension='*.*',
                                    filetypes=[('All files', '*.*')])

        # Browse Entry
        self.fileVar = tk.StringVar()
        self.fileEntry = ttk.Entry(self.Container, width=30)
        self.fileEntry.pack(side='left', anchor='nw', fill='x',
                            expand='yes', padx=5, pady=5)

        # TODO: Copy/paste

        # Browse Button
        try:
            # Use the folder icon
            self.opengif = tk.PhotoImage(file=OPENFOLDER)
            self.browseBut = ttk.Button(self.Container,
                                        command=self._browse)
            self.browseBut.config(image=self.opengif)
        except:
            # Use an elipse
            self.browseBut = ttk.Button(self.Container,
                                        text=" ... ",
                                        command=self._browse)
        self.browseBut.pack(side='right', anchor='ne',
                            padx=5, pady=5)

    def set_parent(self, parent):
        self.root = parent

    def set_filetypes(self, default_ext, types_tupelist):
        self.FILEOPENOPTIONS = None
        self.FILEOPENOPTIONS = dict(defaultextension=default_ext,
                                    filetypes=types_tupelist)

    def _browse(self):
        """Opens file browser and places selected file in entry."""
        browse_file = tkFileDialog.askopenfilenames(
            parent=self.root, **self.FILEOPENOPTIONS)

        # Place in entry box
        # TODO: parent_dir = path.dirname(browse_file)
        self.fileEntry.delete(0, 'end')
        self.fileEntry.insert(0, browse_file)
        self.fileVar.set(browse_file)
        # TODO: return browse_file, parent_dir

    def get(self):
        return self.fileVar.get()


class BrowseDir(ttk.LabelFrame):
    """Select a directory and add it to an entrybox."""
    def __init__(self, root):
        self.root = root
        # Input Frame
        self.Container = ttk.LabelFrame(root,
                                        text=" Select Directory ")
        self.Container.pack(side='top', anchor='n', fill='x',
                            expand='yes', padx=5, pady=5)

        # Browse Entry
        self.fileVar = tk.StringVar()
        self.fileEntry = ttk.Entry(self.Container, width=30)
        self.fileEntry.pack(side='left', anchor='nw', fill='x',
                            expand='yes', padx=5, pady=5)

        # Browse Button
        try:
            # Use the folder icon
            self.opengif = tk.PhotoImage(file=OPENFOLDER)
            self.browseBut = ttk.Button(self.Container, command=self._browse)
            self.browseBut.config(image=self.opengif)
        except:
            # Use an elipse
            self.browseBut = ttk.Button(self.Container, text=" ... ",
                                        command=self._browse)
        self.browseBut.pack(side='right', anchor='ne', padx=5, pady=5)

    def _browse(self):
        """Opens file browser and places selected dir in entry."""
        browse_file = tkFileDialog.askdirectory(parent=self.root)
        self.fileEntry.delete(0, 'end')
        self.fileEntry.insert(0, browse_file)
        self.fileVar.set(browse_file)

    def get(self):
        return self.fileVar.get()


'''
class _App(tk.Frame):
    """Testing GUI"""
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.browse_ent = BrowseFile(self)

        self.browse_ent.set_filetypes('.py',
                                      [('Python', '.pyw'),
                                       ('Python', '.py')])

        self.browse_dir = BrowseDir(self)
'''
'''
if __name__ == '__main__':
    apptools.thread_GUI(_App)
'''


# =============================================================================
# TESTS

def test():
    # Create app
    global app
    app = App("Test App")
    # Create and customize menubar
    menubar = Menubar(None)
    menubar.add_menu("File")
    menubar.menus["File"].add_action("Close", app.close)
    menubar.add_menu("Help")
    menubar.menus["Help"].add_action(
        "About", Popup("About", "This program ...").show_info)
    # Add menubar to app
    app.add_widget(menubar.name, menubar)

    app.add_widget("browser1", BrowseFile(app))
    # Run it
    app.add_button("OK", app.cmd_collect_values)
    app.mainloop()


def thread_test():
    # TODO: tk windows cannot be created after this runs...
    @threaded_gui
    class _TestApp(tk.Frame):
        """ Testing GUI """
        def __init__(self, root):
            """ Parent window properties """
            tk.Frame.__init__(self, root)
            self.root = root
            self.root.protocol("WM_DELETE_WINDOW", self.close)
            self.root.title('Tkit Import Test App')
            resize = True
            if resize is False:
                self.root.resizable(0, 0)
            self.root.lift()
            self.root.focus_force()
            self.root.deiconify()

            """ Widgets """

            # Menubar
            self.menubar = Menubar(self)
            self.menubar.add_menu("File")
            self.menubar.menus["File"].add_action("Close", self.quit)
            self.menubar.add_menu("Edit")
            self.menubar.menus["Edit"].add_action("None", None)
            self.menubar.add_menu("Data")
            self.menubar.add_menu("Tools")
            self.menubar.menus["Tools"].add_action("Import", None)
            self.menubar.menus["Tools"].add_action("Export", None)
            self.menubar.add_submenu("Tools", "Models")
            self.menubar.menus["Tools"].items["Models"].add_action(
                "Building Permits", None)
            self.menubar.add_menu("View")
            self.menubar.menus["View"].add_action("Console", None)
            self.menubar.add_menu("Help")
            self.menubar.menus["Help"].add_action(
                "About", Popup("About", "Stuff").show_info)
            self.menubar.set_parent(self.root)

            # Browse Field
            self.browse_ent = BrowseFile(self)

            self.browse_dir = BrowseDir(self)

            # Print selected browse fields
            self.print_but = ttk.Button(self, text=' Test print ',
                                        command=self.print_dir)
            self.print_but.pack()

            # Status Bar
            self.Ok_but = ttk.Button(self, text=' Test Status ',
                                     command=self.call_main)

            self.statusbar = Statusbar(self, self.Ok_but)

            # Ok button
            self.Ok_but.pack(side='right', anchor='se', padx=5, pady=5)

            # Radiobox
            self.radiobox = Radiobox(self, 'int', ' Wait Time ',
                                     'right', 'nw', 'both', 1)
            self.radiobox.add_button('Five', 5)
            self.radiobox.add_button('Ten', 10)
            self.radiobox.add_button('Fifteen', 15)

            # FileTree
            self.filetree = FileTree(self)

            """ Bindings """

            self.root.bind('<Return>', self.call_main)
            self.root.bind('<Escape>', self.close)

        """ Window Methods """

        def close(self, event=None):
            self.root.destroy()
            self.master.quit()
            return

        """ Main Method(s) """

        def print_dir(self):
            print self.browse_dir.get()
            print self.browse_ent.get()

        def call_main(self, event=None):
            """Threadifies Main() and passes parameters to it."""
            self.main_thread = ThreadedClient(
                "Main", lambda: self.Main(self.radiobox.get()))
            self.main_thread.start()

        def Main(self, t):
            """Emulates process."""
            self.statusbar.start()
            sleep(t)
            self.statusbar.stop()


# Sources:
# https://stackoverflow.com/questions/4297949/image-on-a-button
# https://stackoverflow.com/questions/11352278/default-file-type-in-tkfiledialogs-askopenfilename-method
