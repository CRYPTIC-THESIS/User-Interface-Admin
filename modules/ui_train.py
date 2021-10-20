from tkinter import *
from PIL import ImageTk, Image
from tkcalendar import DateEntry
import pandas as pd
from functools import partial

from assets.elements.tkinter_custom_button import TkinterCustomButton
from assets.elements.treeview import *


# Display Train tab
def train(menuCanvas, color):
    
    menuCanvas.delete('all')
    print('Train')

    menuCanvas.create_text(78, 28, text='TRAIN', font=("Segoe UI bold", 20), fill=color['white'])

    # Display Cards
    cards(menuCanvas, color)


# Cards
def cards(menuCanvas, color):
    global dashCanvas
    dashCanvas = Canvas(menuCanvas, bg=menuCanvas.cget('background'), width=1007, height=548, highlightthickness=0)
    menuCanvas.create_window(535, 335, window=dashCanvas)

    img = Image.open("./assets/images/Base1.png")
    img = img.resize((317, 544), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(img, master=dashCanvas)
    base = Label(dashCanvas, image=test, bg=menuCanvas.cget('background'))
    base.image = test
    dashCanvas.create_image(0,0, anchor=NW, image=test)

    img = img.resize((665, 544), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(img, master=dashCanvas)
    base1 = Label(dashCanvas, image=test, bg=menuCanvas.cget('background'))
    base1.image = test
    dashCanvas.create_image(338,0, anchor=NW, image=test)

    dashCanvas.create_text(17, 13, text='GET DATA', font=("Segoe UI bold", 12), fill=color['white'], anchor=NW)
    dashCanvas.create_text(365, 13, text='DATASET', font=("Segoe UI bold", 12), fill=color['white'], anchor=NW)

    get_data(menuCanvas, color)


# Get Data
def get_data(menuCanvas, color):
    
    # Proceed command
    def proceed():
        # Treeview
        tbldataset = treeview('', 590, 450, 671, 285, dashCanvas)

        # Data Analysis button
        toDataCanvas = Canvas(menuCanvas, bg=menuCanvas.cget('background'), width=204, height=35, highlightthickness=0)
        menuCanvas.create_window(948, 27, window=toDataCanvas, tags='button')

        img = ImageTk.PhotoImage(Image.open('./assets/images/btnDataAnalysis.png'))
        btn = Button(toDataCanvas, command=partial(data_analysis, menuCanvas), bg=color['primary'], bd=0, highlightthickness=0, image=img, activebackground=color['primary'])
        btn.image = img
        btn.place(x=0, y=0)

    
    # Cancel command
    def cancel():
        dashCanvas.delete('all')
        menuCanvas.delete('button')
        get_data(menuCanvas, color)


    btnProceed = TkinterCustomButton(master=dashCanvas, text='PROCEED', text_font=("Segoe UI bold", 11), corner_radius=10,
                width=90, height=35, text_color=color['white'], bg_color=color['light'], fg_color=color['cyan'],
                hover_color=color['green'], command=proceed)
    dashCanvas.create_window(212, 495, anchor=NW, window=btnProceed)

    
    btnCancel = TkinterCustomButton(master=dashCanvas, text='CANCEL', text_font=("Segoe UI bold", 11), corner_radius=10,
                width=85, height=35, text_color=color['white'], bg_color=color['light'], fg_color=color['dark'],
                hover_color=color['red'], command=cancel) #.place(x=110, y=495)
    dashCanvas.create_window(117, 495, anchor=NW, window=btnCancel)


# Data Analysis
def data_analysis(menuCanvas):
    print('hello')
    dashCanvas.delete('all')
    menuCanvas.delete('button')


    # Start Training button
    toTrainingCanvas = Canvas(menuCanvas, bg=menuCanvas.cget('background'), width=204, height=35, highlightthickness=0)
    menuCanvas.create_window(948, 27, window=toTrainingCanvas, tags='button')

    img = ImageTk.PhotoImage(Image.open('./assets/images/btnStartTraining.png'))
    btn = Button(toTrainingCanvas, command=partial(start_training, menuCanvas), bg=color['primary'], bd=0, highlightthickness=0, image=img, activebackground=color['primary'])
    btn.image = img
    btn.place(x=0, y=0)


# Start Training
def start_training(menuCanvas):
    print('hello')
    dashCanvas.delete('all')
    menuCanvas.delete('button')

