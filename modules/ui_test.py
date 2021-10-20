from tkinter import *
from PIL import ImageTk, Image
import pandas as pd
from functools import partial

from assets.elements.tkinter_custom_button import TkinterCustomButton


# Display Test tab
def test(menuCanvas, color):
    menuCanvas.delete('all')
    print('Test')

    menuCanvas.create_text(65, 28, text='TEST', font=("Segoe UI bold", 20), fill=color['white'])

    global dashCanvas
    dashCanvas = Canvas(menuCanvas, bg=menuCanvas.cget('background'), width=1007, height=548, highlightthickness=0)
    menuCanvas.create_window(535, 335, window=dashCanvas)

    # Display Testing
    testing(menuCanvas, color)
    


# Cards
def testing(menuCanvas, color):
    cards('testing', menuCanvas)

    dashCanvas.create_text(28, 15, text='Cryptocurrency', font=("Segoe UI semibold", 12), fill=color['white'], anchor=NW)
    dashCanvas.create_text(258, 15, text='Source', font=("Segoe UI semibold", 12), fill=color['white'], anchor=NW)
    dashCanvas.create_text(562, 15, text='Time Frame', font=("Segoe UI semibold", 12), fill=color['white'], anchor=NW)


def cards(tab, menuCanvas):
    if tab == 'testing':
        img = Image.open("./assets/images/Base1.png")
        img = img.resize((1003, 156), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(img, master=dashCanvas)
        base = Label(dashCanvas, image=test, bg=menuCanvas.cget('background'))
        base.image = test
        dashCanvas.create_image(2,1, anchor=NW, image=test)

        img = img.resize((550, 361), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(img, master=dashCanvas)
        base1 = Label(dashCanvas, image=test, bg=menuCanvas.cget('background'))
        base1.image = test
        dashCanvas.create_image(231,177, anchor=NW, image=test)
    else:
        print(tab)
