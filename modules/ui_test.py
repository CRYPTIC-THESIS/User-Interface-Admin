from tkinter import *
from PIL import ImageTk, Image
import pandas as pd
from functools import partial

from assets.elements.tkinter_custom_button import TkinterCustomButton


# Display Test tab
def test(menuCanvas, color, buttons):
    menuCanvas.delete('all')
    print('Test')

    menuCanvas.create_text(65, 28, text='TEST', font=("Segoe UI bold", 20), fill=color['white'])

    global dashCanvas
    dashCanvas = Canvas(menuCanvas, bg=menuCanvas.cget('background'), width=1007, height=548, highlightthickness=0)
    menuCanvas.create_window(535, 335, window=dashCanvas)

    # Display Testing
    testing(menuCanvas, color, buttons)


# Testing
def testing(menuCanvas, color, buttons):
    cards('testing', menuCanvas)

    dashCanvas.create_text(28, 15, text='Cryptocurrency', font=("Segoe UI semibold", 12), fill=color['white'], anchor=NW)
    dashCanvas.create_text(258, 15, text='Source', font=("Segoe UI semibold", 12), fill=color['white'], anchor=NW)
    dashCanvas.create_text(562, 15, text='Time Frame', font=("Segoe UI semibold", 12), fill=color['white'], anchor=NW)

    
    # Start Testing Command
    def start_testing():
        cards('start', menuCanvas)

        # Data Analysis button
        toDataCanvas = Canvas(menuCanvas, bg=menuCanvas.cget('background'), width=204, height=35, highlightthickness=0)
        menuCanvas.create_window(948, 27, window=toDataCanvas, tags='button')

        img = ImageTk.PhotoImage(Image.open('./assets/images/btnDataAnalysis.png'))
        btn = Button(toDataCanvas, command=partial(data_analysis, menuCanvas), bg=color['primary'], bd=0, highlightthickness=0, image=img, activebackground=color['primary'])
        btn.image = img
        btn.place(x=0, y=0)


    # Get Data Command
    def toTrainTab():
        buttons[1].invoke()


    btnStartTest = TkinterCustomButton(master=dashCanvas, text='START TESTING', text_font=("Segoe UI bold", 11), corner_radius=10,
                width=135, height=35, text_color=color['white'], bg_color=color['light'], fg_color=color['cyan'],
                hover_color=color['green'], command=start_testing)
    dashCanvas.create_window(850, 105, anchor=NW, window=btnStartTest)

    
    btnGetData = TkinterCustomButton(master=dashCanvas, text='GET DATA', text_font=("Segoe UI bold", 11), corner_radius=10,
                width=95, height=35, text_color=color['white'], bg_color=color['light'], fg_color=color['dark'],
                hover_color=color['cyan'], command=toTrainTab)
    dashCanvas.create_window(740, 105, anchor=NW, window=btnGetData)


# Data Analysis
def data_analysis(menuCanvas):
    print('hello')
    dashCanvas.delete('all')
    menuCanvas.delete('button')
    
    cards('data analysis', menuCanvas)


def cards(tab, menuCanvas):
    img = Image.open("./assets/images/Base1.png")

    if tab == 'testing':
        img = img.resize((1003, 156), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(img, master=dashCanvas)
        base = Label(dashCanvas, image=test, bg=menuCanvas.cget('background'))
        base.image = test
        dashCanvas.create_image(2,1, anchor=NW, image=test)
    elif tab == 'start':
        img = img.resize((550, 361), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(img, master=dashCanvas)
        base1 = Label(dashCanvas, image=test, bg=menuCanvas.cget('background'))
        base1.image = test
        dashCanvas.create_image(229,177, anchor=NW, image=test)
    else:
        print(tab)
