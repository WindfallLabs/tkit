""" A label frame containing radiobuttons """
# Dev Notes:
__status__ = 'alpha'
#   Implement m by n matrix style setup
#   Fix horizontal vs vertical orientations
#   Test str vs int variable type uses
#   Consider cleaner __int__ with less args
#   Clean code
#

# Imports
import Tkinter as tk
import ttk

import apptools


class Radiobox(ttk.LabelFrame):
    """ Allows user to easily place radio buttions into a labelframe """
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
        # What if the user wants a grid of radio buttons? N x N or max_row / max_col?
        #alignment_methods = {0: 'horizontal', 1: 'vertical'}
        self.button_alignment = r_alignment
        self.r_column = 0
        self.r_row = 0
        
    def add_button(self, radio_name, in_value):
        """ Adds a new button to the radiobox """
        rbutton = ttk.Radiobutton(self.Container, text=radio_name,
                                  value=in_value, variable=self.radio_value)
        rbutton.grid(column = self.r_column, row = self.r_row)
        if self.button_alignment == 'horizontal':
            self.r_column += 1
        else:
            self.r_row += 1
                
    def get_selected(self):
        """ Returns the value of the selected radiobutton """
        return self.radio_value.get()
        
    def _print_selected(self):
        """ For Testing """
        print self.radio_value.get()

#===================================================================
# End of radiobox Module
#===================================================================
# Test Application code:

class _App(tk.Frame):
    """ Testing GUI """
    def __init__(self, root):
        """ Parent window properties """
        tk.Frame.__init__(self, root)
        self.root = root
        self.root.title("Radiobox Test App")

        """ Widgets """
        
        self.radiobox = Radiobox(self, 'str', " Radios ", 'top', 'nw', 'both', 'yes', 1)
        self.radiobox.add_button('Option 1', 'One')
        self.radiobox.add_button('Option 2', 'Two')
        self.radiobox.add_button('Option 3', 'Three')

        self.Ok_but = ttk.Button(text=" Print ",
                                 command = self.radiobox._print_selected)
        self.Ok_but.pack(side='bottom')
        
        
if __name__ == '__main__':
    apptools.thread_GUI(_App)
