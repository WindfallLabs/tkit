import Tkinter as tk
import ttk
import threading
import logging
from time import sleep

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s')


class Statusbar(tk.Frame):
    """ Places status bar and label in frame """
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
        
        self.bar.pack(side='bottom', anchor='s',
                            fill='x', expand='yes',
                            padx=0, pady=0)
        
        self.status_label = ttk.Label(self.bar,
                                      text=self.labels[0])
        self.status_label.pack(side='left', anchor='sw',
                               padx=2, pady=5)
                
        self.progressbar = ttk.Progressbar(self.bar, orient='horizontal',
                                           length=200, mode='indeterminate')

        self.reset_but = tk.Button(self.bar, text="Reset", command=self.reset)
        #self.reset_but.pack(side='right')
        self.reset_but.config(relief='flat',
                              overrelief="groove",
                              height=0)

    def reset(self):
        self.root_but.config(state="enabled")
        self.progressbar.pack_forget()
        self.update_bar()
        self.status_thread = ThreadedClient("Statusbar", self.start_bar)
        self.wait_event = threading.Event()
        self.reset_but.pack_forget()

    def update_bar(self):
        """ changes status label and packs/unpacks progress bar """
        self.cur_status += 1
        if self.cur_status > 2:
            self.cur_status = 0
        self.status_label.config(text=self.labels[self.cur_status])
        if self.cur_status == 1:
            self.progressbar.pack(side='right', expand='y',
                               fill='x', padx=5, pady=2)
        elif self.cur_status == 2:
            self.reset_but.pack(side='right')
            #self.progressbar.pack_forget() # Issue here
            pass

    def start_bar(self):
        self.root_but.config(state="disabled")
        self.progressbar.start(1)
        self.wait_event.wait()
        logging.debug("Status wait event done")
        self.progressbar.stop()
        logging.debug("Bar stopped")

    def start(self):
        self.update_bar()
        self.status_thread.start()

    def stop(self):
        self.wait_event.set()
        self.update_bar()
        #

class ThreadedClient(threading.Thread):
    def __init__(self, name, process):
        """ Subclass of thread allows for easier thread creation """
        threading.Thread.__init__(self)
        self.name = name
        self.process = process
        
    def run(self):
        """ Wait for event to be set before doing anything """
        logging.debug('{0} thread started'.format(self.name))
        self.process()
        logging.debug('{0} thread terminated'.format(self.name))
        

#===================================================================
# End of StatusBar Module -- to be imported
#===================================================================
# Application code:
#import Statusbar

class TestApp(tk.Frame):
    """ Testing GUI """
    def __init__(self, root):
        """ Parent window properties """
        
        tk.Frame.__init__(self, root)
        self.root = root
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

    def call_main(self, *event):
        """ Threadifies Main() and passes parameters to it """
        self.main_thread = ThreadedClient("Main",
                                          lambda: self.Main(self.Main_val))
        self.main_thread.start()


    def Main(self, t):
        """ emulates process """
        logging.debug('Processing...')
        self.statusbar.start()
        sleep(t)
        logging.debug('Processing Complete')
        self.statusbar.stop() # Should also hide/pack_forget the prog bar
        

def build_GUI():
    root = tk.Tk()
    TestApp(root).pack(fill='both', expand='yes')
    root.title("App")
    root.mainloop()

if __name__ == '__main__':
    GUI = ThreadedClient("GUI", build_GUI)
    GUI.start()
    GUI.join()
