import Tkinter as tk
import ttk, tkMessageBox, tkFileDialog

# RadioBox (done)
class RadioBox(ttk.LabelFrame):
    ''' Allows user to easily place radio buttions into a labelframe '''
    def __init__(self, root, str_var, labelframe_text, box_side, box_anchor, box_fill, box_expand, box_padx, box_pady, r_alignment = 'horizontal'):
        # Container
        self.Container = ttk.LabelFrame(root, text=labelframe_text) 
        self.Container.pack(fill=box_fill, expand=box_expand, side=box_side, anchor=box_anchor, padx=box_padx, pady=box_pady)
        # Default radiobutton value   
        self.radio_value = tk.IntVar() #str_var
        #self.radio_value.set('None')
        # Alignment method for radio buttons ('horizontal' or 'vertical')
        # What if the user wants a grid of radio buttons? N x N or max_row / max_col?
        #alignment_methods = {0: 'horizontal', 1: 'vertical'}
        self.button_alignment = r_alignment
        self.r_column = 0
        self.r_row = 0
        
    def add_button(self, radio_name, in_value):
        rbutton = ttk.Radiobutton(self.Container, text=radio_name, value=in_value, variable=self.radio_value)
        rbutton.grid(column = self.r_column, row = self.r_row)
        if self.button_alignment == 'horizontal':
            self.r_column += 1
        else:
            self.r_row += 1
                
    def get_selected(self):
        return self.radio_value.get()
        
    def print_selected(self):
        ''' For Testing '''
        print self.radio_value.get()


# Testing GUI
class TestApp(tk.Frame):
    ''' Testing GUI '''
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.rOption = tk.StringVar()
        self.rOption.set('None')
        radiobox = RadioBox(self, self.rOption, ' Radios ', 'top', 'nw', 'both', 'yes', 5, 5, 1)
        radiobox.add_button('Option 1', 'One')
        radiobox.add_button('Option 2', 'Two')
        radiobox.add_button('Option 3', 'Three')
        
        
if __name__ == '__main__':
    root = tk.Tk()
    TestApp(root).pack(fill='both', expand=True)
    root.title('Test App')
    root.mainloop()
