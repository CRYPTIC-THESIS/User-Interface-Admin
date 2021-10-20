from tkinter import *
from PIL import ImageTk, Image
from tkcalendar import DateEntry
import pandas as pd
import dbconnect as db
from datetime import datetime
from datetime import timedelta

from assets.elements.tkinter_custom_button import TkinterCustomButton
from assets.elements.treeview import *

selected_date = '05/31/2021'

def dashboard(menuCanvas, color):
    
    def selected_date():
        global selected_date
        selected_date = date.get()
       #print(selected_date)

    # Display Dashboard
    menuCanvas.delete('all')
    print('Dashboard')

    menuCanvas.create_text(155, 28, text='CRYPTOCURRENCY', font=("Segoe UI bold", 20), fill=color['white'])

    # Pick Date
    global train_from_range, train_until_range
    train_from_range = pd.to_datetime("01-01-2020")
    train_until_range = pd.to_datetime("05-31-2021")

    dateCanvas = Canvas(menuCanvas, bg=menuCanvas.cget('background'), width=240, height=35, highlightthickness=0)
    menuCanvas.create_window(880, 35, window=dateCanvas)

    date = DateEntry(dateCanvas, width=15, bd=10, font=('Segoe UI semibold', 13), background=color['dark'],
                        mindate=train_from_range, maxdate=train_until_range, date_pattern="mm/dd/y")
    date.place(x=0, y=3)

    img = ImageTk.PhotoImage(Image.open('./assets/images/btnCalendar.png'))
    btnCalendar = Button(dateCanvas, bg=menuCanvas.cget('background'), bd=0, highlightthickness=0, image=img, 
                        activebackground=menuCanvas.cget('background'), command=selected_date)
    btnCalendar.image = img
    btnCalendar.place(x=175, y=0)

    # Crypto Buttons
    btnCanvas = Canvas(menuCanvas, bg=menuCanvas.cget('background'), width=240, height=45, highlightthickness=0)
    menuCanvas.create_window(153, 75, window=btnCanvas)

    btn_ = [
        "./assets/images/btnDashAll.png", "./assets/images/btnBitcoin.png", 
        "./assets/images/btnEthereum.png", "./assets/images/btnDogecoin.png"
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
    img = Image.open("./assets/images/Base.png")
    img = img.resize((533, 311), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(img, master=dashCanvas)
    base = Label(dashCanvas, image=test, bg=menuCanvas.cget('background'))
    base.image = test
    base.place(x=0, y=0)

    Label(dashCanvas, text='PREDICTED PRICES', font=("Segoe UI bold", 12), bg=color['light'],
            fg=color['white']).place(x=25, y=13)


    # Closing, High, Low
    btnCanvas = Canvas(dashCanvas, bg=color['light'], width=231, height=26, highlightthickness=0)
    btnCanvas.place(x=273, y=14)
    prices(btnCanvas, color, color['cyan'])


    # Days Slider
    slider_canvas = Canvas(dashCanvas, width=250, height=40, highlightthickness=0, bg=color['light'])#
    slider_canvas.place(x=25, y=260)

    current_value = DoubleVar()
    def get_current_value():
        return '{: .2f}'.format(current_value.get())

    def slider_changed(event):
        print(int(round(float(get_current_value()))))

    Label(slider_canvas,text='Days:', font=("Segoe UI semibold", 10), bg=color['light'] , fg='white').place(x=0, y=16)

    Scale(slider_canvas, from_=1, to=14, orient='horizontal', sliderrelief='flat', variable=current_value, bg=color['light'],
            command=slider_changed,length=205, fg='white', troughcolor=color['cyan'], highlightthickness=0).place(x=40, y=0)


# Predicted Prices Table card
def price_tbl(menuCanvas, color):
    img = Image.open("./assets/images/Base.png")
    img = img.resize((533, 154), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(img, master=dashCanvas)
    base1 = Label(dashCanvas, image=test, bg=menuCanvas.cget('background'))
    base1.image = test
    base1.place(x=0, y=332)

    # Treeview
    tblprice = treeview('Predicted ____ Price', 490, 110, 267, 408, dashCanvas)


# History card
def history(menuCanvas, color):
    img = Image.open("./assets/images/Base1.png")
    img = img.resize((450, 486), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(img, master=dashCanvas)
    base2 = Label(dashCanvas, image=test, bg=menuCanvas.cget('background'))
    base2.image = test
    base2.place(x=553, y=0)


    # Current Price
    Label(dashCanvas, text='CURRENT PRICE', font=("Segoe UI bold", 12), bg=color['light'],
            fg=color['white']).place(x=578, y=13)
    
    currPriceCanvas = Canvas(dashCanvas, bg=color['light'], width=418.34, height=123, highlightthickness=0)
    dashCanvas.create_window(782, 110, window=currPriceCanvas)
    
    btc_card = TkinterCustomButton(master=currPriceCanvas, hover=False, text='', width=418, height=35.38, corner_radius=10, bg_color=color['light'], fg_color='#41464E')
    eth_card = TkinterCustomButton(master=currPriceCanvas, hover=False, text='', width=418, height=35.38, corner_radius=10, bg_color=color['light'], fg_color='#41464E')
    doge_card = TkinterCustomButton(master=currPriceCanvas, hover=False, text='', width=418, height=35.38, corner_radius=10, bg_color=color['light'], fg_color='#41464E')

    currPriceCanvas.create_window(209, 17, window=btc_card, tags='btc')
    currPriceCanvas.create_window(209, 61, window=eth_card, tags='eth')
    currPriceCanvas.create_window(209, 105, window=doge_card, tags='doge')


    # History
    Label(dashCanvas, text='HISTORY', font=("Segoe UI bold", 12), bg=color['light'],
            fg=color['white']).place(x=578, y=193)


    # Closing, High, Low
    btnCanvas = Canvas(dashCanvas, bg=color['light'], width=231, height=26, highlightthickness=0)
    btnCanvas.place(x=758, y=194)
    prices(btnCanvas, color, color['purple'])     
        
    # Days
    dayBtnCanvas = Canvas(dashCanvas, bg=color['light'], width=170, height=27, highlightthickness=0)
    dayBtnCanvas.place(x=582, y=445)

    data = db.get_data_table('Twitter_Data')

    def select(btn , i):
        def select_button():
            for other_btn in buttons:
                deactivate(other_btn)
            btn.config(bg=color['purple'], activebackground=color['purple'])
            global end_date,start_date
            #if 3 Days is selected
            if (i==0):
                end_date = datetime.strptime(selected_date,'%m/%d/%Y')
                start_date = end_date - timedelta(2)
                print ('From:' + str(start_date) + ' To:' + str(end_date))
            #if 1 Week is selected
            elif (i==1):
                end_date = datetime.strptime(selected_date,'%m/%d/%Y')
                start_date = end_date - timedelta(6)
                print ('From:' + str(start_date) + ' To:' + str(end_date))
            #if 1 Month is selected
            elif (i==2):
                end_date = datetime.strptime(selected_date,'%m/%d/%Y')
                start_date = end_date - timedelta(29)
                print ('From:' + str(start_date) + ' To:' + str(end_date))
            #if 1 Year is selected
            elif (i==3):
                end_date = datetime.strptime(selected_date,'%m/%d/%Y')
                start_date = end_date - timedelta(364)
                print ('From:' + str(start_date) + ' To:' + str(end_date))
        return select_button

    def deactivate(btn):
        btn.config(bg='#41464E', activebackground=color['purple'])

    list_ = ['3D', '1W', '1M', '1Y']
    buttons = []

    x=0
    for i, name in enumerate(list_, 0):
        btn = Button(dayBtnCanvas, text=name, font=("Segoe UI bold", 10), width=3, bd=0, highlightthickness=0, 
                        foreground=color['white'], activeforeground=color['white']) 
        btn['command'] = select(btn , i)
        btn.place(x=x, y=0)
        buttons.append(btn)
        x+=35
    buttons[0].invoke()


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
