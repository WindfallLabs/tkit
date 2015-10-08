# Tk GUI Classes

# Imports
import Tkinter as tk
import tkMessageBox
import tkFileDialog
import os

#import apptools

class Menubar(tk.Menu):
    def __init__(self, root):
        tk.Menu.__init__(self, root)
        self.root = root
        
        """ File Menu """
        self.File = NewMenu(self)
        self.add_cascade(label="File",underline=0, menu=self.File)
        self.File.add_command(label="Exit", underline=1, command=self.quit)
        
        """ Tools """
        self.Help = NewMenu(self)
        self.add_cascade(label="Help", underline=0, menu=self.Help)
        #self.HelpSub = SubMenu(self.Help, "Help Sub")
        # Arc Tools sub-menu
        #tools_garc = NewMenu(self)
        #self.Help.add_cascade(label="GArc Tools", underline=1, menu=tools_garc)
        #tools_garc.add_command(label="Reset Arc GUI", command=None)
        # Design sub-menu
        #tools_design = NewMenu(self)
        #self.Help.add_cascade(label="Design", underline=0, menu=tools_design)

    """ Window methods """
    
    def quit(self):
        self.root.destroy()


class NewMenu(tk.Menu):
    def __init__(self, root):
        tk.Menu.__init__(self, root, tearoff=False)


        
class SubMenu(tk.Menu):
    def __init__(self, parent_menu, submenu_name):
        #tk.Menu.__init__(self, parent_menu, tearoff=False)
        self.parent = parent_menu
        self.sub_menu = NewMenu(parent_menu)
        self.sub_menu.add_cascade(label=submenu_name)
        

#===================================================================
# End of browse_entry Module
#===================================================================
# Test Application code:
class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        menubar = Menubar(self)
        self.config(menu=menubar)
        self.geometry("200x0")

if __name__ == "__main__":
    app=App()
    app.mainloop()
