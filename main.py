from tkinter import *
from modules.ui_main import ui

# Window
root = Tk()
root.overrideredirect(True)
root.geometry('1280x720+25+20')
root['bg'] = '#282c34'

# Display Interface
ui(root)

# Start the app
root.mainloop()