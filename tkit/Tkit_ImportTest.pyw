import threading
import Queue
import Tkinter as tk
import ttk, tkFileDialog, tkMessageBox

try:
    from BrowseField import *
    from FileTree import *
    from RadioBox import *
    #from StatusBar import *
    from StatusBar_Alpha import *
except:
    print "Failed to import Tkit contents"


# Testing GUI
class TestApp(tk.Frame):
    ''' Testing GUI '''
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        
        
        
        ''' Window Properties '''
        root.title('Testing window')
        #root.geometry('200x150')
        resize = True
        if resize == False:
            root.resizable(0,0)
        root.lift()
        root.focus_force()
        root.deiconify()

        ''' Layout '''
        # Browse Field
        BrowseField(self)
        
        # Status Bar
        self.statusbar = Statusbar(self)
        
        self.radiobox = RadioBox(self, 5, 'top', 'right', 'n', 'both', 5, 5, 1)
        self.radiobox.add_button('Five', 5)
        self.radiobox.add_button('Fifteen', 15)
        #self.radiobox.add_button('Option 3', 'Three')
        
        
        # Show r_value button

        FileTree(self)
        
        #showbutton = ttk.Button(self, text='Show Value', command=radiobox.print_selected)
        self.Ok_but = ttk.Button(self, text=' Test Status ', command=self.call_main)
        self.Ok_but.pack(side = 'bottom', anchor = 'se', padx=5, pady=5)
        
        #self.prog_bar = ttk.Progressbar(self, orient="horizontal", mode="indeterminate")
        #self.prog_bar.pack(side='top', fill='x', expand='yes')

    def call_main(self, *event):
        """ Threadifies Main() and passes parameters to it """
        self.main_thread = ThreadedClient("Main",
                                          lambda: self.Main(self.radiobox.get_selected()))
        self.main_thread.start()

    def Main(self, t):
        """ emulates process """
        self.Ok_but.config(state="disabled")
        self.statusbar.start()
        sleep(t)
        self.statusbar.stop()

def build_GUI():
    root = tk.Tk()
    TestApp(root).pack(fill='both', expand='yes')
    root.title("TestApp")
    root.mainloop()

if __name__ == '__main__':
    GUI = threading.Thread(name="GUI", target=build_GUI)
    GUI.start()
    GUI.join()
