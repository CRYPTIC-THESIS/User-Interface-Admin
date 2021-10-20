from tkinter import *
from PIL import ImageTk, Image
from tkcalendar import DateEntry
import pandas as pd


def dashboard(menuCanvas, color):
    # Display Dashboard
    menuCanvas.delete('all')
    print('Dashboard')

    # title = Label(menuCanvas, text='CRYPTOCURRENCY', font=("Segoe UI bold", 20), bg=menuCanvas.cget('background'),
    #                 fg=color['white'])
    # menuCanvas.create_window(150, 30, window=title)
    menuCanvas.create_text(155, 28, text='CRYPTOCURRENCY', font=("Segoe UI bold", 20), fill=color['white'])

    # Pick Date
    global train_from_range, train_until_range
    train_from_range = pd.to_datetime("01-01-2020")
    train_until_range = pd.to_datetime("05-31-2021")

    dateCanvas = Canvas(menuCanvas, bg=menuCanvas.cget('background'), width=240, height=35, highlightthickness=0)
    menuCanvas.create_window(880, 35, window=dateCanvas)

    date = DateEntry(dateCanvas, width=15, bd=10, font=('Segoe UI semibold', 13), background=color['dark'],
                        mindate=train_from_range, maxdate=train_until_range, date_pattern="mm/dd/y").place(x=0, y=3)

    img = ImageTk.PhotoImage(Image.open('./images/btnCalendar.png'))
    btnCalendar = Button(dateCanvas, bg=menuCanvas.cget('background'), bd=0, highlightthickness=0, image=img, 
                        activebackground=menuCanvas.cget('background'))
    btnCalendar.image = img
    btnCalendar.place(x=175, y=0)
    

    # Crypto Buttons
    btnCanvas = Canvas(menuCanvas, bg=menuCanvas.cget('background'), width=240, height=45, highlightthickness=0)
    menuCanvas.create_window(153, 75, window=btnCanvas)

    btn_ = [
        "./images/btnDashAll.png", "./images/btnBitcoin.png", 
        "./images/btnEthereum.png", "./images/btnDogecoin.png"
    ]
    buttons = []
    
    x = 0
    for i, name in enumerate(btn_):
        img = ImageTk.PhotoImage(Image.open(name))
        btn = Button(btnCanvas, bg=menuCanvas.cget('background'), bd=0, highlightthickness=0, image=img, 
                        activebackground=menuCanvas.cget('background'))
        btn.image = img
        #btn['command'] = graph(btn, i)
        btn.place(x=x, y=0)
        buttons.append(btn)
        x+=65
    buttons[0].invoke()


    # Cards
    global dashCanvas
    dashCanvas = Canvas(menuCanvas, bg=menuCanvas.cget('background'), width=1007, height=490, highlightthickness=0)
    menuCanvas.create_window(535, 365, window=dashCanvas)

    predicted_prices(menuCanvas, color)
    price_tbl(menuCanvas, color)
    history(menuCanvas, color)


# Predicted Price card
def predicted_prices(menuCanvas, color):
    img = Image.open("./images/Base.png")
    img = img.resize((533, 311), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(img, master=dashCanvas)
    base = Label(dashCanvas, image=test, bg=menuCanvas.cget('background'))
    base.image = test
    base.place(x=0, y=0)

    Label(dashCanvas, text='PREDICTED PRICES', font=("Segoe UI bold", 12), bg=color['light'],
            fg=color['white']).place(x=25, y=13)


# Predicted Prices Table card
def price_tbl(menuCanvas, color):
    img = Image.open("./images/Base.png")
    img = img.resize((533, 154), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(img, master=dashCanvas)
    base1 = Label(dashCanvas, image=test, bg=menuCanvas.cget('background'))
    base1.image = test
    base1.place(x=0, y=332)


# History card
def history(menuCanvas, color):
    img = Image.open("./images/Base1.png")
    img = img.resize((450, 486), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(img, master=dashCanvas)
    base2 = Label(dashCanvas, image=test, bg=menuCanvas.cget('background'))
    base2.image = test
    base2.place(x=553, y=0)


    # Current Price
    Label(dashCanvas, text='CURRENT PRICE', font=("Segoe UI bold", 12), bg=color['light'],
            fg=color['white']).place(x=578, y=13)
    
    