import pandas as pd
import dbconnect as db

from tkinter import *
from PIL import ImageTk, Image
from tkcalendar import DateEntry
from functools import partial
from assets.elements.tkinter_custom_button import TkinterCustomButton
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
    from_date = '2020-01-01'
    to_date = '2020-01-31'
    if (selected_crypto=='Bitcoin'):
        crypto_data = pd.DataFrame(db.get_data_table('Bitcoin_Data'))
        crypto_data['date'] = pd.to_datetime(crypto_data['date'])
        crypto_data = crypto_data.loc[(crypto_data['date'] >= from_date) & (crypto_data['date'] <= to_date)]
        if (selected_sources == 'Bitcoin_Data, Twitter_Data, Reddit_Data, Google_Data'):
            #Twitter
            twitter_data = pd.DataFrame(db.get_data_table('Twitter_Data'))
            twitter_data['date'] = pd.to_datetime(twitter_data['date'],infer_datetime_format='%Y-%m-%d')
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

    dashCanvas.create_text(17, 13, text='GET DATA', font=("Segoe UI bold", 12), fill=color['white'], anchor=NW)
    dashCanvas.create_text(365, 13, text='DATASET', font=("Segoe UI bold", 12), fill=color['white'], anchor=NW)
    
    # Proceed command
    def proceed():
        # Treeview
        tbldataset = treeview('', 590, 450, 671, 285, dashCanvas)

        # Data Analysis button
        toDataCanvas = Canvas(menuCanvas, bg=menuCanvas.cget('background'), width=204, height=35, highlightthickness=0)
        menuCanvas.create_window(948, 27, window=toDataCanvas, tags='button')

        img = ImageTk.PhotoImage(Image.open('./assets/images/btnDataAnalysis.png'))
        btn = Button(toDataCanvas, bg=color['primary'], bd=0, highlightthickness=0, image=img, activebackground=color['primary'], command= select_data) #<=== Changed command
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
    
    cards('data analysis', menuCanvas)


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


# Cards
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
    elif tab == 'data analysis':
        print(tab)
    else:
        print('training data')
    