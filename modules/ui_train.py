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
def select_data(crypto, source, from_date, to_date):
    print('Hello Select Data')

    df = pd.DataFrame(columns=['Date'])

    table_name = {
        'BITCOIN': 'btc', 'ETHEREUM': 'eth', 'DOGECOIN': 'doge',
        'Bitcoin_data': 'Bitcoin_Data', 'Ethereum_data': 'Ethereum_Data', 'Dogecoin_data': 'Dogecoin_Data',
        'Twitter Volume': 'Twitter_Data', 'Reddit Volume': 'Reddit_Data', 'Google Trends': 'Google_Data'
    }
    
    for item in source:
        if item == 'Twitter Volume':
            twitter = pd.DataFrame(db.get_data_table(table_name[item]))
            twitter = twitter[['date', table_name[crypto]]]
            twitter['date'] = pd.to_datetime(twitter['date'])
            twitter = twitter.loc[(twitter['date'] >= from_date) & (twitter['date'] <= to_date)]
            twitter.columns=['Date', item]
            # print(twitter)
            # df = pd.concat([df, twitter], ignore_index=True)
            df = pd.merge(df, twitter, how='outer', on='Date')
        
        elif item == 'Reddit Volume':
            reddit = pd.DataFrame(db.get_data_table(table_name[item]))
            reddit = reddit[['date', table_name[crypto]]]
            reddit['date'] = pd.to_datetime(reddit['date'])
            reddit = reddit.loc[(reddit['date'] >= from_date) & (reddit['date'] <= to_date)]
            reddit.columns=['Date', item]
            # df = pd.concat([df, reddit], ignore_index=True)
            df = pd.merge(df, reddit, how='outer', on='Date')
        
        elif item == 'Google Trends':
            google = pd.DataFrame(db.get_data_table(table_name[item]))
            google = google[['date', table_name[crypto]]]
            google['date'] = pd.to_datetime(google['date'])
            google = google.loc[(google['date'] >= from_date) & (google['date'] <= to_date)]
            google.columns=['Date', item]
            # df = pd.concat([df, google], ignore_index=True)
            df = pd.merge(df, google, how='outer', on='Date')
        
        elif item == 'CoinDesk Historical Data':
            if table_name[crypto] == 'btc':
                historical = 'Bitcoin_Data'
            elif table_name[crypto] == 'eth':
                historical = 'Ethereum_Data'
            else:
                historical = 'Dogecoin_Data'
            crypto_data = pd.DataFrame(db.get_data_table(historical))
            crypto_data['date'] = pd.to_datetime(crypto_data['date'])
            crypto_data = crypto_data.loc[(crypto_data['date'] >= from_date) & (crypto_data['date'] <= to_date)]
            crypto_data.columns=['Date', 'High', 'Low', 'Open', 'Closing']
            # df = pd.concat([crypto_data, df], ignore_index=True)
            df = pd.merge(crypto_data, df, how='outer', on='Date')

    crypto_ = []
    for rows in range(len(df)):
        if table_name[crypto] == 'btc':
            crypto_.append('BTC')
        elif table_name[crypto] == 'eth':
            crypto_.append('ETH')
        else:
            crypto_.append('DOGE')

    df.insert(0, "Cryptocurrency", crypto_, True)

    print('dataframe', df)

    # final_df = pd.DataFrame(columns=["Date", "High", "Low", "Open Price", "Closing Price", "Twitter_Data", "Reddit_Data", "Google_Data"])
    # final_df = pd.merge([crypto_data,twitter,reddit,google],axis = 1)
    # print(final_df)
    return df


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
            # if item.get() == 'CoinDesk Historical Data':
            #     for crypto in crypto_data_list:
            #         if crypto == 'BITCOIN':
            #             source_data_list.append('Bitcoin_data')
            #         elif crypto == 'ETHEREUM':
            #             source_data_list.append('Ethereum_data')
            #         elif crypto == 'DOGECOIN':
            #             source_data_list.append('Dogecoin_data')
            # el
            if item.get() != "":
                source_data_list.append(item.get())
        print("Sources: ", source_data_list)


        from_this_date = from_date.get()
        until_this_date = until_date.get()
        print("From: ",from_this_date)
        print("Until: ",until_this_date)


        # Treeview
        tbldataset = treeview('', 590, 450, 671, 285, dashCanvas)

        my_df = pd.DataFrame()
        for crypto in crypto_data_list:
            print(crypto)
            my_df = pd.concat([my_df, select_data(crypto, source_data_list, from_this_date, until_this_date)], ignore_index=True)
        print(my_df.head())
        my_df['Date'] = my_df['Date'].dt.date

        # Displaying the DataFrame
        tbldataset["column"] = list(my_df.columns)
        tbldataset["show"] = "headings"
        for column in tbldataset["columns"]:
            tbldataset.heading(column, text=column) 
            tbldataset.column(column, width=165,anchor="center")

        df_rows = my_df.to_numpy().tolist() 
        for row in df_rows:
            tbldataset.insert("", "end", values=row, tags=("row"))

        tbldataset.tag_configure("row", foreground=color['white'])


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
    