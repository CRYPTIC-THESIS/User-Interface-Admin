from tkinter import *
from PIL import ImageTk, Image
import pandas as pd

from modules.tkinter_custom_button import TkinterCustomButton

def deploy(menuCanvas, color):
    # Display Deploy tab
    menuCanvas.delete('all')
    print('Test')

    menuCanvas.create_text(80, 28, text='DEPLOY', font=("Segoe UI bold", 20), fill=color['white'])


    # Cards
    global dashCanvas
    dashCanvas = Canvas(menuCanvas, bg=menuCanvas.cget('background'), width=1007, height=548, highlightthickness=0)
    menuCanvas.create_window(535, 335, window=dashCanvas)

    dataset(menuCanvas, color)
    predicted_prices(menuCanvas, color)
    price_tbl(menuCanvas, color)


# Dataset card
def dataset(menuCanvas, color):
    img = Image.open("./images/Base1.png")
    img = img.resize((1003, 156), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(img, master=dashCanvas)
    base = Label(dashCanvas, image=test, bg=menuCanvas.cget('background'))
    base.image = test
    base.place(x=0, y=0)


    # Display Dataset
    Label(dashCanvas, text='Cryptocurrency', font=("Segoe UI semibold", 12), bg=color['light'],
            fg=color['white']).place(x=25, y=13)
    
    Label(dashCanvas, text='Source', font=("Segoe UI semibold", 12), bg=color['light'],
            fg=color['white']).place(x=255, y=13)

    Label(dashCanvas, text='Time Frame', font=("Segoe UI semibold", 12), bg=color['light'],
            fg=color['white']).place(x=559, y=13)


# Predicted Prices card
def predicted_prices(menuCanvas, color):
    img = Image.open("./images/Base1.png")
    img = img.resize((666, 367), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(img, master=dashCanvas)
    base1 = Label(dashCanvas, image=test, bg=menuCanvas.cget('background'))
    base1.image = test
    base1.place(x=0, y=177)


    # Predicted Price
    Label(dashCanvas, text='PREDICTED PRICES', font=("Segoe UI bold", 12), bg=color['light'],
            fg=color['white']).place(x=25, y=192)

    btnCanvas = Canvas(dashCanvas, bg=color['light'], width=231, height=26, highlightthickness=0)
    btnCanvas.place(x=408, y=195)
    prices(btnCanvas, color, color['cyan'])

    
    # Days Slider
    slider_canvas = Canvas(dashCanvas, width=270, height=40, highlightthickness=0, bg=color['light'])#
    slider_canvas.place(x=25, y=490)

    current_value = DoubleVar()
    def get_current_value():
        return '{: .2f}'.format(current_value.get())

    def slider_changed(event):
        print(int(round(float(get_current_value()))))

    Label(slider_canvas,text='Days:', font=("Segoe UI semibold", 10), bg=color['light'] , fg='white').place(x=0, y=16)

    Scale(slider_canvas, from_=1, to=14, orient='horizontal', sliderrelief='flat', variable=current_value, bg=color['light'],
            command=slider_changed,length=220, fg='white', troughcolor=color['cyan'], highlightthickness=0).place(x=45, y=0)


# Predicted Prices Table card
def price_tbl(menuCanvas, color):
    img = Image.open("./images/Base.png")
    img = img.resize((317, 367), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(img, master=dashCanvas)
    base2 = Label(dashCanvas, image=test, bg=menuCanvas.cget('background'))
    base2.image = test
    base2.place(x=686, y=177)

    


# Closing, High, Low buttons
def prices(canvas, color, text_color):
    closing = TkinterCustomButton(master=canvas, text='Closing', text_font=("Segoe UI semibold", 11), corner_radius=32,
                width=86, height=26, text_color=text_color, bg_color=color['light'], fg_color=color['light'],
                hover_color='white')
    
    high = TkinterCustomButton(master=canvas, text='High', text_font=("Segoe UI semibold", 11), corner_radius=32,
                width=65, height=26, text_color=text_color, bg_color=color['light'], fg_color=color['light'],
                hover_color='white')

    low = TkinterCustomButton(master=canvas, text='Low', text_font=("Segoe UI semibold", 11), corner_radius=32,
                width=60, height=26, text_color=text_color, bg_color=color['light'], fg_color=color['light'],
                hover_color='white')

    canvas.create_window(43, 13, window=closing, tags='closing')
    canvas.create_window(128.45, 13, window=high, tags='high')
    canvas.create_window(201, 13, window=low, tags='low')
