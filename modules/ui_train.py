from tkinter import *
from PIL import ImageTk, Image
from tkcalendar import DateEntry
import pandas as pd

from assets.elements.tkinter_custom_button import TkinterCustomButton
from assets.elements.treeview import *


def train(menuCanvas, color):
    # Display Train tab
    menuCanvas.delete('all')
    print('Train')

    menuCanvas.create_text(78, 28, text='TRAIN', font=("Segoe UI bold", 20), fill=color['white'])

    # Cards
    global dashCanvas
    dashCanvas = Canvas(menuCanvas, bg=menuCanvas.cget('background'), width=1007, height=548, highlightthickness=0)
    menuCanvas.create_window(535, 335, window=dashCanvas)

    dataset(menuCanvas, color)
    data_tbl(menuCanvas, color)

    # img = Image.open("./images/Base1.png")
    # img = img.resize((665, 544), Image.ANTIALIAS)
    # test = ImageTk.PhotoImage(img, master=dashCanvas)
    # base1 = Label(dashCanvas, image=test, bg=menuCanvas.cget('background'))
    # base1.image = test
    # base1.place(x=338, y=0)


def dataset(menuCanvas, color):
    img = Image.open("./assets/images/Base1.png")
    img = img.resize((317, 544), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(img, master=dashCanvas)
    base = Label(dashCanvas, image=test, bg=menuCanvas.cget('background'))
    base.image = test
    base.place(x=0, y=0)

    Label(dashCanvas, text='GET DATA', font=("Segoe UI bold", 12), bg=color['light'],
            fg=color['white']).place(x=15, y=13)

    # Proceed
    def proceed():
        # Treeview
        tbldataset = treeview('', 590, 450, 671, 285, dashCanvas)

        # Data Analysis button


    TkinterCustomButton(master=dashCanvas, text='PROCEED', text_font=("Segoe UI bold", 11), corner_radius=10,
                width=90, height=35, text_color=color['white'], bg_color=color['light'], fg_color=color['cyan'],
                hover_color=color['green'], command=proceed).place(x=212, y=495)


    # Cancel
    def cancel():
        dashCanvas.delete('all')

    TkinterCustomButton(master=dashCanvas, text='CANCEL', text_font=("Segoe UI bold", 11), corner_radius=10,
                width=85, height=35, text_color=color['white'], bg_color=color['light'], fg_color=color['dark'],
                hover_color=color['red'], command=cancel).place(x=110, y=495)


def data_tbl(menuCanvas, color):
    img = Image.open("./assets/images/Base1.png")
    img = img.resize((665, 544), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(img, master=dashCanvas)
    base1 = Label(dashCanvas, image=test, bg=menuCanvas.cget('background'))
    base1.image = test
    base1.place(x=338, y=0)

    Label(dashCanvas, text='DATASET', font=("Segoe UI bold", 12), bg=color['light'],
            fg=color['white']).place(x=363, y=13)