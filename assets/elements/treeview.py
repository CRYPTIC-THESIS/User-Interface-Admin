from tkinter import *
from PIL import ImageTk, Image
from tkinter import ttk

# Color
color = {
    'primary': '#282c34',
    'white': '#dddddd',
    'dark': '#21252b',
    'light': '#2c313a',
    'cyan': '#259CA5',
    'purple': '#8C88BF'
}

def treeview(title, width, height, x, y, container):
    my_frame = LabelFrame(container,text=title, fg="white", highlightthickness=0, width=width, height=height, bg=color['light'])
    container.create_window(x,y, window=my_frame, tags=('canvas'))


    tv_canvas = Canvas(my_frame,highlightthickness=0, width=width, height=height)
    my_treeview = ttk.Treeview(tv_canvas)
    my_treeview.place(relheight=1,relwidth=1)
    yscroll = Scrollbar(my_frame, orient="vertical")
    xscroll = Scrollbar(my_frame, orient="horizontal")
            
    yscroll.configure(command=my_treeview.yview)
    xscroll.configure(command=my_treeview.xview)

    my_treeview.configure(xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
    yscroll.pack(side=RIGHT,fill=Y)
    xscroll.pack(side=BOTTOM,fill=X)
    tv_canvas.pack(side=LEFT,expand=True,fill=BOTH)
            
    style = ttk.Style(tv_canvas)
    style.theme_use("clam")
    style.configure("Treeview", background="#404C62",
                foreground="white", fieldbackground='#94B0B3')
    style.map('Treeview', background=[('selected',color['cyan'])], foreground=[('selected',"white")])

    style.configure("Treeview.Heading", background="white",
                foreground="black")#, relief="flat"

    return my_treeview