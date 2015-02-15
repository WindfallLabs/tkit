import Tkinter as tk
import ttk

# Consider "ProcessingQueue" as name
class FileTree(ttk.LabelFrame):
    ''' Allows user to easily manipulate columns of data '''
    def __init__(self, root):
        #self.framelabel = labelframe_text
        #self.columns = column_num
        #
        self.container = ttk.LabelFrame(root, text=' Tabel Label ')
        self.container.pack(side='top', anchor='n', fill='x', expand='yes', padx=5, pady=5)
        self.headers = "Col 1"
        self.build_tree()
        self.add_controls()
        
    def build_tree(self):
        tree = ttk.Treeview(self.container, show="headings",height=5)
        tree["columns"] = "single"
        tree.column("single", width=200)
        tree.heading("single", text="Input Files")
        tree.pack(fill='x')

    def add_controls(self):
        ''' Controls for manipulating Tree contents '''
        # Add button - adds table contents
        self.AddBut = ttk.Button(self.container, text='Add')
        self.AddBut.pack(side='left')
        # Remove button - removes selected table contents
        self.RemoveBut = ttk.Button(self.container, text='Remove')
        self.RemoveBut.pack(side='right')
   
        
# Testing GUI
class TestApp(tk.Frame):
    ''' Testing GUI '''
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        FileTree(self)
        
        
        
if __name__ == '__main__':
    root = tk.Tk()
    TestApp(root).pack(fill='both', expand=True)
    root.title('Test App')
    root.mainloop()

    
"""
root = tk.Tk()
tree = ttk.Treeview(root, show="headings")

tree["columns"] = "single"
tree.column("single", width=200)
tree.heading("single", text="Input Files")

#tree.insert("", 0, text="Line 1", value="Garin")


def add_rows(num):
    row_count = 0
    while row_count <= num:
        tree.insert("", row_count, text="Line %i" % row_count, value="")
        row_count += 1
        
#add_rows(5)

tree.pack()
root.mainloop()
"""
