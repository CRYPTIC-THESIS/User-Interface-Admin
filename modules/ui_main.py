from tkinter import *
from PIL import Image, ImageTk
import pandas as pd
from tkcalendar import DateEntry

from assets.elements.tkinter_custom_button import *
from modules.ui_dash import *
from modules.ui_deploy import *
from modules.ui_train import *
from modules.ui_test import *



# Color
color = {
    'primary': '#282c34',
    'white': '#dddddd',
    'dark': '#21252b',
    'light': '#2c313a',
    'cyan': '#259CA5',
    'purple': '#8C88BF',
    'green': '#30960C',
    'red': '#B20D0D'
}

def ui(root):

    # Display Titlebar
    customTitlebar(root)

    # Display Sidebar Menu
    sidebarMenu(root)


def customTitlebar(root):
    # Custom Titlebar
    titlebar = Frame(root, bg=color['dark'], relief='raised', bd=0, highlightthickness=0, width=1280, height=50)
    titlebar.place(x=0, y=0)

    Frame(root, bg=color['light'], relief='raised', bd=0, highlightthickness=0, width=1280, height=7).place(x=0, y=50)

    close_button = Button(titlebar, text='  X  ', bg=color['dark'], font=("calibri", 13),bd=0,fg='white',highlightthickness=0)
    close_button.configure(command=root.destroy)
    close_button.place(x=1240, y=10)

    minimize_button = Button(titlebar, text='  ─  ',bg=color['dark'],bd=0, fg='white',font=("calibri", 13),highlightthickness=0)
    minimize_button.place(x=1200, y=10)

    logo = Image.open("./assets/images/Logo.png")
    img = ImageTk.PhotoImage(logo)
    logo = Label(titlebar, image=img, bg=color['dark'])
    logo.image = img
    logo.place(x=18, y=3)

    titlebar_title = Label(titlebar, text='Welcome to CRYPTIC!', bg=color['dark'], bd=0,fg=color['white'],
                        font=("Segoe UI semibold", 11),highlightthickness=0)
    titlebar_title.place(x=222, y=13)

    # Exit and Minimize Binding
    def minimize_me(event):
        # minimize_button['bg']='blue'
        root.update_idletasks()
        root.update()
        root.overrideredirect(False)
        # root.state('iconic')
        root.iconify()

    def get_pos(event):
        xwin = root.winfo_x()
        ywin = root.winfo_y()
        startx = event.x_root
        starty = event.y_root

        ywin = ywin - starty
        xwin = xwin - startx

        def move_window(event):
            root.update_idletasks()
            root.geometry('+{0}+{1}'.format(event.x_root + xwin, event.y_root + ywin))
        startx = event.x_root
        starty = event.y_root

        titlebar.bind('<B1-Motion>', move_window)
    titlebar.bind('<Button-1>', get_pos)

    def frame_mapped(e):
        root.update_idletasks()
        root.overrideredirect(True)
        root.state('normal')

    titlebar.bind('<B1-Motion>', get_pos)
    close_button.bind('<Enter>', lambda _: close_button.config(bg='red'))
    close_button.bind('<Leave>', lambda _: close_button.config(bg=titlebar.cget('background')))
    minimize_button.bind('<Enter>', lambda _: minimize_button.config(bg=color['light']))
    minimize_button.bind('<Leave>', lambda _: minimize_button.config(bg=titlebar.cget('background')))
    minimize_button.bind('<Button-1>', minimize_me)    
    titlebar.bind("<Map>",frame_mapped)

def sidebarMenu(root):
    # Sidebar Menu
    def select(btn, i):
        def select_button():
            for other_btn in buttons:
                deactivate(other_btn)
            btn.config(bg='#252930')

            # Display Selected Menu
            # ///////////////////////////////////// 
            global menuCanvas
            menuCanvas = Canvas(root, bg=color['primary'], width=1073, height=643, highlightthickness=0)
            menuCanvas.place(x=197,y=67)
    
            if i == 0:
                dashboard(menuCanvas, color)
            elif i == 1:
                train(menuCanvas, color)
            elif i == 2:
                test(menuCanvas, color, buttons)
            else:
                deploy(menuCanvas, color)
                   
        return select_button

    def deactivate(btn):
        btn.config(bg=color['dark'], activebackground='#252930')

    btn_ = [
        "./assets/images/btnDash.png", "./assets/images/btnTrain.png", "./assets/images/btnTest.png",
        "./assets/images/btnDeploy.png"
    ]
    buttons = []

    sidebar = Frame(root, bg=color['dark'], relief='raised', bd=0, highlightthickness=0, width=187, height=663)
    sidebar.place(x=0, y=57)

    y = 0
    for i, name in enumerate(btn_):
        img = ImageTk.PhotoImage(Image.open(name))
        btn = Button(sidebar, bg=color['dark'], bd=0, highlightthickness=0, image=img, activebackground='#252930')
        btn.image = img
        btn['command'] = select(btn, i)
        btn.place(x=0, y=y)
        buttons.append(btn)
        y+=59
    
    buttons[0].invoke()
