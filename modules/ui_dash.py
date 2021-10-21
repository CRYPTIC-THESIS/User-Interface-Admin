from tkinter import *
from PIL import ImageTk, Image
from tkcalendar import DateEntry
from functools import partial
from datetime import datetime
from datetime import timedelta

import dbconnect as db
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from assets.elements.tkinter_custom_button import TkinterCustomButton
from assets.elements.treeview import *


def dashboard(menuCanvas, color):
    # Display Dashboard
    menuCanvas.delete('all')
    print('Dashboard')

    menuCanvas.create_text(155, 28, text='CRYPTOCURRENCY', font=("Segoe UI bold", 20), fill=color['white'])


    # Get Date command
    def get_date():
        global selected_date
        selected_date = date.get()
        selected_date = pd.to_datetime(selected_date)
        print(selected_date)

        try:
            buttons[1].invoke()
        except Exception:
            pass



    # Selected Cryptocurrency command
    def get_crypto(i):
        def select_button():
            # Dashboard content
            global dashCanvas
            dashCanvas = Canvas(menuCanvas, bg=menuCanvas.cget('background'), width=1007, height=490, highlightthickness=0)
            menuCanvas.create_window(535, 365, window=dashCanvas)

            predicted_card(menuCanvas, color)
            price_tbl(menuCanvas, color)
            history_card(menuCanvas, color)

            if i == 0:
                selected_crypto = 'all'
                print('all crypto dash')
                currPriceCanvas.delete('all')
                history_card(menuCanvas, color)

            elif i == 1:
                selected_crypto = 'BTC'
                print('btc dash')
                currPriceCanvas.delete('all')
                history_card(menuCanvas, color)
                currPriceCanvas.delete('btc')
                btc_card = TkinterCustomButton(master=currPriceCanvas, hover=False, text='', width=418, height=35.38, corner_radius=10, bg_color=color['light'], fg_color=color['cyan'])
                currPriceCanvas.create_window(209, 17, window=btc_card, tags=('btc',))
            
            elif i == 2:
                selected_crypto = 'ETH'
                print('eth dash')
                currPriceCanvas.delete('all')
                history_card(menuCanvas, color)
                currPriceCanvas.delete('eth')
                eth_card = TkinterCustomButton(master=currPriceCanvas, hover=False, text='', width=418, height=35.38, corner_radius=10, bg_color=color['light'], fg_color=color['cyan'])
                currPriceCanvas.create_window(209, 61, window=eth_card, tags=('eth',))

            else:
                selected_crypto = 'DOGE'
                print('doge dash')
                currPriceCanvas.delete('all')
                history_card(menuCanvas, color)
                currPriceCanvas.delete('doge')
                doge_card = TkinterCustomButton(master=currPriceCanvas, hover=False, text='', width=418, height=35.38, corner_radius=10, bg_color=color['light'], fg_color=color['cyan'])
                currPriceCanvas.create_window(209, 105, window=doge_card, tags=('doge',))


            def default_btn(canvas, text_color, command):
                canvas.delete('all')

                closing = TkinterCustomButton(master=canvas, text='Closing', text_font=("Segoe UI semibold", 11), corner_radius=32,
                            width=86, height=26, text_color=text_color, bg_color=color['light'], fg_color=color['light'],
                            hover_color='white', command=partial(command, canvas, text_color, 0))
                
                high = TkinterCustomButton(master=canvas, text='High', text_font=("Segoe UI semibold", 11), corner_radius=32,
                            width=65, height=26, text_color=text_color, bg_color=color['light'], fg_color=color['light'],
                            hover_color='white', command=partial(command, canvas, text_color, 1))

                low = TkinterCustomButton(master=canvas, text='Low', text_font=("Segoe UI semibold", 11), corner_radius=32,
                            width=60, height=26, text_color=text_color, bg_color=color['light'], fg_color=color['light'],
                            hover_color='white', command=partial(command, canvas, text_color, 2))

                canvas.create_window(43, 13, window=closing, tags='closing')
                canvas.create_window(128.45, 13, window=high, tags='high')
                canvas.create_window(201, 13, window=low, tags='low')

            
            # Create Graph
            # df2 - dataframe
            # i - btn index
            # w, h - width, height
            # plot - 'Date'
            # x, y - placement for graph
            def graph(df2, i, w, h, plot, x, y):
                figure2 = plt.Figure(figsize=(w, h), dpi=100, facecolor=color['light'])
                ax2 = figure2.add_subplot(111)

                if i == 2 or i == 3:
                    df2.plot(x=plot, kind='line', legend=True, ax=ax2, color="#4ad29f", fontsize=7)
                else:
                    df2.plot(x=plot, kind='line', legend=True, ax=ax2, color="#4ad29f", marker='o',fontsize=7)

                ax2.set_facecolor(color['light'])
                ax2.xaxis.label.set_color('w')
                ax2.yaxis.grid(color=color['dark'],linewidth=1)

                for label in ax2.xaxis.get_ticklabels():
                    label.set_color('w')
                for label in ax2.yaxis.get_ticklabels():
                    label.set_color('w')

                ax2.spines['bottom'].set_color(color['dark'])
                ax2.spines['top'].set_color(color['dark'])
                ax2.spines['left'].set_color(color['dark'])
                ax2.spines['right'].set_color(color['dark'])

                line2 = FigureCanvasTkAgg(figure2, graph_canvas)
                line2 = line2.get_tk_widget()
                graph_canvas.create_window(x, y, window=line2, anchor=NW, tags=('graph',))

            
            # Predicted Prices
            def predicted(canvas, text_color, i):
                global price
                # Button Activate
                if i == 0:
                    price = 'Closing'
                    default_btn(canvas, text_color, predicted)
                    canvas.delete(price)
                    closing = TkinterCustomButton(master=canvas, text='Closing', text_font=("Segoe UI semibold", 11), corner_radius=32,
                            width=86, height=26, text_color=text_color, bg_color=color['light'], fg_color='white',
                            hover_color='white', command=partial(predicted, canvas, text_color, 0))
                    canvas.create_window(43, 13, window=closing, tags='closing')

                elif i == 1:
                    price = 'High'
                    default_btn(canvas, text_color, predicted)
                    canvas.delete(price)
                    high = TkinterCustomButton(master=canvas, text='High', text_font=("Segoe UI semibold", 11), corner_radius=32,
                            width=65, height=26, text_color=text_color, bg_color=color['light'], fg_color='white',
                            hover_color='white', command=partial(predicted, canvas, text_color, 1))
                    canvas.create_window(128.45, 13, window=high, tags='high')

                else:
                    price = 'Low'
                    default_btn(canvas, text_color, predicted)
                    canvas.delete(price)
                    low = TkinterCustomButton(master=canvas, text='Low', text_font=("Segoe UI semibold", 11), corner_radius=32,
                            width=60, height=26, text_color=text_color, bg_color=color['light'], fg_color='white',
                            hover_color='white', command=partial(predicted, canvas, text_color, 2))
                    canvas.create_window(201, 13, window=low, tags='low')


            btnCanvas = Canvas(dashCanvas, bg=color['light'], width=231, height=26, highlightthickness=0)
            btnCanvas.place(x=273, y=14)
            default_btn(btnCanvas, color['cyan'], predicted)
            predicted(btnCanvas, color['cyan'], 0)


            # History
            def history(canvas, text_color, i):
                global price
                # Button Activate
                if i == 0:
                    price = 'Closing'
                    default_btn(canvas, text_color, history)
                    canvas.delete(price)
                    closing = TkinterCustomButton(master=canvas, text='Closing', text_font=("Segoe UI semibold", 11), corner_radius=32,
                            width=86, height=26, text_color=text_color, bg_color=color['light'], fg_color='white',
                            hover_color='white', command=partial(history, canvas, text_color, 0))
                    canvas.create_window(43, 13, window=closing, tags='closing')

                elif i == 1:
                    price = 'High'
                    default_btn(canvas, text_color, history)
                    canvas.delete(price)
                    high = TkinterCustomButton(master=canvas, text='High', text_font=("Segoe UI semibold", 11), corner_radius=32,
                            width=65, height=26, text_color=text_color, bg_color=color['light'], fg_color='white',
                            hover_color='white', command=partial(history, canvas, text_color, 1))
                    canvas.create_window(128.45, 13, window=high, tags='high')

                else:
                    price = 'Low'
                    default_btn(canvas, text_color, history)
                    canvas.delete(price)
                    low = TkinterCustomButton(master=canvas, text='Low', text_font=("Segoe UI semibold", 11), corner_radius=32,
                            width=60, height=26, text_color=text_color, bg_color=color['light'], fg_color='white',
                            hover_color='white', command=partial(history, canvas, text_color, 2))
                    canvas.create_window(201, 13, window=low, tags='low')


                # Selected History days
                # //////////////////////////////
                def select(btn, i):
                    def select_button():
                        for other_btn in buttons:
                            deactivate(other_btn)
                        btn.config(bg=color['purple'], activebackground=color['purple'])

                        # Get history
                        if i == 0:
                            days = 3
                        elif i == 1:
                            days = 7
                        elif i == 2:
                            days = 30
                        else:
                            days = 365

                        global past
                        past = selected_date - timedelta(days=days)
                        print(past)


                        # Dataframe
                        my_df = pd.DataFrame()
                        btc_df = pd.DataFrame()
                        eth_df = pd.DataFrame()
                        doge_df = pd.DataFrame()
                        
                        crypto_data = [ 'Bitcoin_Data', 'Ethereum_Data', 'Dogecoin_Data']
                        # crypto = []

                        if selected_crypto == 'all':
                            crypto = []
                            for j, crypto_ in enumerate(crypto_data):
                                db_data = pd.DataFrame(db.get_data_table(crypto_))
                                db_data['date'] = pd.to_datetime(db_data['date'])
                                db_data = db_data.loc[(db_data['date'] >= past) & (db_data['date'] <= selected_date)]

                                for rows in range(len(db_data)):
                                    if j == 0:
                                        crypto.append('BTC')
                                    elif j == 1:
                                        crypto.append('ETH')
                                    else:
                                        crypto.append('DOGE')

                                my_df = pd.concat([my_df,db_data], ignore_index=True)

                                if j == 0:
                                    btc_df = db_data
                                elif j == 1:
                                    eth_df = db_data
                                else:
                                    doge_df = db_data

                            my_df.insert(0, "Cryptocurrency", crypto, True)
                            my_df.columns = [ 'Cryptocurrency', 'Date', "High", "Low", "Open", "Closing"]
                            print(my_df.head(10))

                            df = my_df[['Cryptocurrency', 'Date', price]].copy(deep=True)
                            print(df.head(10))
                        
                        else:
                            if selected_crypto == 'BTC':
                                j = 0
                            elif selected_crypto == 'ETH':
                                j = 1
                            else:
                                j = 2
                            
                            crypto = []
                            db_data = pd.DataFrame(db.get_data_table(crypto_data[j]))
                            db_data['date'] = pd.to_datetime(db_data['date'])
                            db_data = db_data.loc[(db_data['date'] >= past) & (db_data['date'] <= selected_date)]

                            for rows in range(len(db_data)):
                                if j == 0:
                                    crypto.append('BTC')
                                elif j == 1:
                                    crypto.append('ETH')
                                else:
                                    crypto.append('DOGE')

                            my_df = pd.concat([my_df,db_data], ignore_index=True)

                            my_df.insert(0, "Cryptocurrency", crypto, True)
                            my_df.columns = [ 'Cryptocurrency', 'Date', "High", "Low", "Open", "Closing"]
                            print(my_df.head(10))

                            df = my_df[['Cryptocurrency', 'Date', price]].copy(deep=True)
                            print(df.head(10))

                            
                            df[price] = pd.to_numeric(df[price])
                            df2 = df[['Date',price]]
                            x = 'Date'
                            print('df2')
                                
                            graph(df2, i, 4.6, 2.35, x, -15, -23)
                        
                        
                    return select_button

                def deactivate(btn):
                    btn.config(bg='#41464E', activebackground=color['purple'])

                # Buttons
                dayBtnCanvas = Canvas(dashCanvas, bg=color['light'], width=170, height=27, highlightthickness=0)
                dayBtnCanvas.place(x=582, y=445)
                list_ = ['3D', '1W', '1M', '1Y']
                buttons = []

                x=0
                for i, name in enumerate(list_, 0):
                    btn = Button(dayBtnCanvas, text=name, font=("Segoe UI bold", 10), width=3, bd=0, highlightthickness=0, 
                                    foreground=color['white'], activeforeground=color['white']) 
                    btn['command'] = select(btn, i)
                    btn.place(x=x, y=0)
                    buttons.append(btn)
                    x+=35
                buttons[0].invoke()


            # Graph canvas
            graph_canvas = Canvas(dashCanvas, width=412, height=207, highlightthickness=0, bg=color['purple'])
            dashCanvas.create_window(574, 230, anchor=NW, window=graph_canvas)

            btnCanvas = Canvas(dashCanvas, bg=color['light'], width=231, height=26, highlightthickness=0)
            btnCanvas.place(x=758, y=194)
            default_btn(btnCanvas, color['cyan'], history)
            history(btnCanvas, color['purple'], 0)

        return select_button


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
                        activebackground=menuCanvas.cget('background'), command=get_date)
    btnCalendar.image = img
    btnCalendar.place(x=175, y=0)
    # /////// Get the initial date
    btnCalendar.invoke()


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
        btn['command'] = get_crypto(i)
        btn.place(x=x, y=0)
        buttons.append(btn)
        x+=65
    # /////// All cryptocurrency dashboard
    buttons[1].invoke()


# ----------- CARDS -------------
def predicted_card(menuCanvas, color):
    img = Image.open("./assets/images/Base.png")
    img = img.resize((533, 311), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(img, master=dashCanvas)
    base = Label(dashCanvas, image=test, bg=menuCanvas.cget('background'))
    base.image = test
    base.place(x=0, y=0)

    Label(dashCanvas, text='PREDICTED PRICES', font=("Segoe UI bold", 12), bg=color['light'],
            fg=color['white']).place(x=25, y=13)

def price_tbl(menuCanvas, color):
    img = Image.open("./assets/images/Base.png")
    img = img.resize((533, 154), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(img, master=dashCanvas)
    base1 = Label(dashCanvas, image=test, bg=menuCanvas.cget('background'))
    base1.image = test
    base1.place(x=0, y=332)

def history_card(menuCanvas, color):
    img = Image.open("./assets/images/Base1.png")
    img = img.resize((450, 486), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(img, master=dashCanvas)
    base2 = Label(dashCanvas, image=test, bg=menuCanvas.cget('background'))
    base2.image = test
    base2.place(x=553, y=0)


    # Current Price
    Label(dashCanvas, text='CURRENT PRICE', font=("Segoe UI bold", 12), bg=color['light'],
            fg=color['white']).place(x=578, y=13)
    
    global currPriceCanvas
    currPriceCanvas = Canvas(dashCanvas, bg=color['light'], width=418.34, height=123, highlightthickness=0)
    dashCanvas.create_window(782, 110, window=currPriceCanvas)
    
    btc_card = TkinterCustomButton(master=currPriceCanvas, hover=False, text='', width=418, height=35.38, corner_radius=10, bg_color=color['light'], fg_color='#41464E')
    eth_card = TkinterCustomButton(master=currPriceCanvas, hover=False, text='', width=418, height=35.38, corner_radius=10, bg_color=color['light'], fg_color='#41464E')
    doge_card = TkinterCustomButton(master=currPriceCanvas, hover=False, text='', width=418, height=35.38, corner_radius=10, bg_color=color['light'], fg_color='#41464E')

    currPriceCanvas.create_window(209, 17, window=btc_card, tags=('btc',))
    currPriceCanvas.create_window(209, 61, window=eth_card, tags=('eth',))
    currPriceCanvas.create_window(209, 105, window=doge_card, tags=('doge',))

    Label(dashCanvas, text='HISTORY', font=("Segoe UI bold", 12), bg=color['light'],
            fg=color['white']).place(x=578, y=193)