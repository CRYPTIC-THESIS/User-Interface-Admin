from tkinter import font
import pandas as pd
import dbconnect as db

from tkinter import *
from PIL import ImageTk, Image
from tkcalendar import DateEntry
from functools import partial
from assets.elements.tkinter_custom_button import TkinterCustomButton as tkButton
from assets.elements.treeview import *


# Display Train tab
def train(menuCanvas, color):
    menuCanvas.delete('all')
    print('Train')

    menuCanvas.create_text(78, 28, text='TRAIN', font=("Segoe UI bold", 20), fill=color['white'])

    global dashCanvas
    dashCanvas = Canvas(menuCanvas, bg=menuCanvas.cget('background'), width=1007, height=548, highlightthickness=0)
    menuCanvas.create_window(535, 335, window=dashCanvas)

    # Display Get Data
    get_data(menuCanvas, color)

#Selection of Data
def select_data():
    print('Hello Select Data')
    selected_crypto = 'Bitcoin'
    selected_sources = 'Bitcoin_Data, Twitter_Data, Reddit_Data, Google_Data'
    from_date = '2020-02-01'
    to_date = '2020-02-29'
    if (selected_crypto=='Bitcoin'):
        crypto_data = pd.DataFrame(db.get_data_table('Bitcoin_Data'))
        crypto_data['date'] = pd.to_datetime(crypto_data['date'])
        crypto_data = crypto_data.loc[(crypto_data['date'] >= from_date) & (crypto_data['date'] <= to_date)]
        if (selected_sources == 'Bitcoin_Data, Twitter_Data, Reddit_Data, Google_Data'):
            #Twitter
            twitter_data = pd.DataFrame(db.get_data_table('Twitter_Data'))
            twitter_data['date'] = pd.to_datetime(twitter_data['date'])
            twitter_data = twitter_data.loc[(twitter_data['date'] >= from_date) & (twitter_data['date'] <= to_date)]
            #Reddit
            reddit_data = pd.DataFrame(db.get_data_table('Reddit_Data'))
            reddit_data['date'] = pd.to_datetime(reddit_data['date'])
            reddit_data = reddit_data.loc[(reddit_data['date'] >= from_date) & (reddit_data['date'] <= to_date)]
            #Google
            google_data = pd.DataFrame(db.get_data_table('Google_Data'))
            google_data['date'] = pd.to_datetime(google_data['date'])
            google_data = google_data.loc[(google_data['date'] >= from_date) & (google_data['date'] <= to_date)]

            final_df = pd.concat([crypto_data,twitter_data[['btc']],reddit_data[['btc']],google_data[['btc']]],axis = 1)
            final_df.columns = ["Date", "High", "Low", "Open Price", "Closing Price", "Twitter_Data", "Reddit_Data", "Google_Data"]
            print(final_df)

# Get Data
def get_data(menuCanvas, color):
    cards('get data', menuCanvas)

    # Checkbox
    data = [
        "BITCOIN", "ETHEREUM", "DOGECOIN",
        "CoinDesk Historical Data", "Twitter Volume",
        "Reddit Volume", "Google Trends"
    ]

    crypto_list = []
    source_list = []


    # Proceed command
    def proceed():
        global crypto_data_list, source_data_list
        global from_this_date, until_this_date

        crypto_data_list = []
        for item in crypto_list:
            if item.get() != "":
                crypto_data_list.append(item.get())
        print("Crypto: ", crypto_data_list)


        source_data_list = []
        for item in source_list:
            if item.get() != "":
                source_data_list.append(item.get())
        print("Sources: ", source_data_list)


        from_this_date = from_date.get()
        until_this_date = until_date.get()
        print("From: ",from_this_date)
        print("Until: ",until_this_date)


        # Treeview
        tbldataset = treeview('', 590, 450, 671, 285, dashCanvas)

        # Start Training button
        toTrainingCanvas = Canvas(menuCanvas, bg=menuCanvas.cget('background'), width=204, height=35, highlightthickness=0)
        menuCanvas.create_window(948, 27, window=toTrainingCanvas, tags='button')

        img = ImageTk.PhotoImage(Image.open('./assets/images/btnStartTraining.png'))
        btn = Button(toTrainingCanvas, command=partial(start_training,menuCanvas), bg=color['primary'], bd=0, highlightthickness=0, image=img, activebackground=color['primary'])
        #btn = Button(toTrainingCanvas, command=select_data, bg=color['primary'], bd=0, highlightthickness=0, image=img, activebackground=color['primary'])
        btn.image = img
        btn.place(x=0, y=0)

    
    # Cancel command
    def cancel():
        dashCanvas.delete('all')
        menuCanvas.delete('button')
        get_data(menuCanvas, color)


    # Select Time Frame
    global train_from_range, train_until_range
    train_from_range = pd.to_datetime("01-01-2020")
    train_until_range = pd.to_datetime("05-31-2021")

    dashCanvas.create_text(50, 100, text='FROM:', font=("Segoe UI semibold", 12), fill=color['white'], anchor=NW)
    dashCanvas.create_text(50, 129, text='UNTIL:', font=("Segoe UI semibold", 12), fill=color['white'], anchor=NW)
    
    from_date = DateEntry(dashCanvas, width=15, bd=10, font=('Segoe UI semibold', 12), background=color['dark'],
                        mindate=train_from_range, maxdate=train_until_range, date_pattern="mm/dd/y")
    dashCanvas.create_window(120, 95, window=from_date, anchor=NW)

    until_date = DateEntry(dashCanvas, width=15, bd=10, font=('Segoe UI semibold', 12), background=color['dark'],
                        mindate=train_from_range, maxdate=train_until_range, date_pattern="mm/dd/y")
    dashCanvas.create_window(120, 127, window=until_date, anchor=NW)


    # Select Cryptocurrency
    y=213
    for i in range(3):
        var = StringVar()
        check = Checkbutton(dashCanvas, text=data[i], font=('Segoe UI semibold', 12), variable=var, fg=color['white'],  relief=FLAT, activeforeground=color['white'],
                    onvalue=data[i],offvalue='',bg=color['light'],activebackground=color['light'], selectcolor='#41464E')
        dashCanvas.create_window(48, y, window=check, anchor=NW)
        y+=27
        crypto_list.append(var)

    
    # Select Source
    y=350
    for i in range(3,7):
        var = StringVar()
        check = Checkbutton(dashCanvas, text=data[i], font=('Segoe UI semibold', 12), variable=var, fg=color['white'],  relief=FLAT, activeforeground=color['white'],
                    onvalue=data[i],offvalue='',bg=color['light'],activebackground=color['light'], selectcolor='#41464E')
        dashCanvas.create_window(48, y, window=check, anchor=NW)
        y+=27
        source_list.append(var)


    btnProceed = tkButton(master=dashCanvas, text='PROCEED', text_font=("Segoe UI bold", 11), corner_radius=10,
                width=90, height=35, text_color=color['white'], bg_color=color['light'], fg_color=color['cyan'],
                hover_color=color['green'], command=proceed)
    dashCanvas.create_window(212, 495, anchor=NW, window=btnProceed)

    
    btnCancel = tkButton(master=dashCanvas, text='CANCEL', text_font=("Segoe UI bold", 11), corner_radius=10,
                width=85, height=35, text_color=color['white'], bg_color=color['light'], fg_color=color['dark'],
                hover_color=color['red'], command=cancel) #.place(x=110, y=495)
    dashCanvas.create_window(117, 495, anchor=NW, window=btnCancel)


# Start Training
def start_training(menuCanvas):
    print('hello')
    dashCanvas.delete('all')
    menuCanvas.delete('button')


# ----------- CARDS -------------
def cards(tab, menuCanvas):
    if tab == 'get data':
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

        card = tkButton(master=dashCanvas, hover=False, text='Time Frame', width=286, height=35.38, corner_radius=10, 
                            bg_color=color['light'], fg_color='#41464E', text_font=("Segoe UI semibold", 10))
        dashCanvas.create_window(15, 47, window=card, anchor=NW)
        
        card = tkButton(master=dashCanvas, hover=False, text='Cryptocurrency', width=286, height=35.38, corner_radius=10, 
                            bg_color=color['light'], fg_color='#41464E', text_font=("Segoe UI semibold", 10))
        dashCanvas.create_window(15, 175, window=card, anchor=NW)

        card = tkButton(master=dashCanvas, hover=False, text='Source', width=286, height=35.38, corner_radius=10, 
                            bg_color=color['light'], fg_color='#41464E', text_font=("Segoe UI semibold", 10))
        dashCanvas.create_window(15, 310, window=card, anchor=NW)

    elif tab == 'data analysis':
        print(tab)
    else:
        print('training data')
    