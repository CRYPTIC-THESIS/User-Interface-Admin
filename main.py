from tkinter import *
from modules.ui_main import ui

# Window
root = Tk()
root.geometry('1280x720')
root['bg'] = '#282c34'

# Display Interface
ui(root)

# Start the app
root.mainloop()