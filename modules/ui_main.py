from tkinter import *
from PIL import Image, ImageTk
import pandas as pd
from tkcalendar import DateEntry

# Color
color = {
    'primary': '#282c34',
    'white': '#dddddd',
    'dark': '#21252b',
    'light': '#2c313a'
}

def ui(root):
    print('hello')

    # Display Titlebar
    customTitlebar(root)

    # Display Sidebar Menu
    sidebarMenu(root)


def customTitlebar(root):
    # Custom Titlebar
    titlebar = Frame(root, bg=color['dark'], relief='raised', bd=0, highlightthickness=0, width=1280, height=50)
    titlebar.place(x=0, y=0)

    Frame(root, bg=color['light'], relief='raised', bd=0, highlightthickness=0, width=1280, height=7).place(x=0, y=50)

    close_button = Button(titlebar, text='  X  ', bg=color['dark'], font=("calibri", 13),bd=0,fg='white',highlightthickness=0)
    close_button.configure(command=root.destroy)
    close_button.place(x=1240, y=10)

    minimize_button = Button(titlebar, text='  ─  ',bg=color['dark'],bd=0, fg='white',font=("calibri", 13),highlightthickness=0)
    minimize_button.place(x=1200, y=10)

    logo = Image.open("images/Logo.png")
    img = ImageTk.PhotoImage(logo)
    logo = Label(titlebar, image=img, bg=color['dark'])
    logo.image = img
    logo.place(x=18, y=3)

    titlebar_title = Label(titlebar, text='Welcome to CRYPTIC!', bg=color['dark'], bd=0,fg=color['white'],
                        font=("Segoe UI semibold", 11),highlightthickness=0)
    titlebar_title.place(x=222, y=13)

    # Exit and Minimize Binding
    def minimize_me(event):
        # minimize_button['bg']='blue'
        root.update_idletasks()
        root.overrideredirect(False)
        root.state('iconic')

    def get_pos(event):
        xwin = root.winfo_x()
        ywin = root.winfo_y()
        startx = event.x_root
        starty = event.y_root

        ywin = ywin - starty
        xwin = xwin - startx

        def move_window(event):
            root.update_idletasks()
            root.geometry('+{0}+{1}'.format(event.x_root + xwin, event.y_root + ywin))
        startx = event.x_root
        starty = event.y_root

        titlebar.bind('<B1-Motion>', move_window)
    titlebar.bind('<Button-1>', get_pos)

    def frame_mapped(e):
        root.update_idletasks()
        root.overrideredirect(True)
        root.state('normal')

    titlebar.bind('<B1-Motion>', get_pos)
    close_button.bind('<Enter>', lambda _: close_button.config(bg='red'))
    close_button.bind('<Leave>', lambda _: close_button.config(bg=titlebar.cget('background')))
    minimize_button.bind('<Enter>', lambda _: minimize_button.config(bg=color['light']))
    minimize_button.bind('<Leave>', lambda _: minimize_button.config(bg=titlebar.cget('background')))
    minimize_button.bind('<Button-1>', minimize_me)    
    titlebar.bind("<Map>",frame_mapped)

def sidebarMenu(root):
    # Sidebar Menu
    def select(btn, i):
        def select_button():
            for other_btn in buttons:
                deactivate(other_btn)
            btn.config(bg='#252930')

            # Display Selected Menu
            # ///////////////////////////////////// 
            global menuCanvas
            menuCanvas = Canvas(root, bg=color['primary'], width=1073, height=643, highlightthickness=0)
            menuCanvas.place(x=197,y=67)
    
            if i == 0:
                dashboard()
            elif i == 1:
                train()
            elif i == 2:
                test()
            else:
                deploy()
                   
        return select_button

    def deactivate(btn):
        btn.config(bg=color['dark'], activebackground='#252930')

    btn_ = [
        "images/btnDash.png", "images/btnTrain.png", "images/btnTest.png",
        "images/btnDeploy.png"
    ]
    buttons = []

    sidebar = Frame(root, bg=color['dark'], relief='raised', bd=0, highlightthickness=0, width=187, height=663)
    sidebar.place(x=0, y=57)

    y = 0
    for i, name in enumerate(btn_):
        img = ImageTk.PhotoImage(Image.open(name))
        btn = Button(sidebar, bg=color['dark'], bd=0, highlightthickness=0, image=img, activebackground='#252930')
        btn.image = img
        btn['command'] = select(btn, i)
        btn.place(x=0, y=y)
        buttons.append(btn)
        y+=59
    
    buttons[0].invoke()

def dashboard():
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

    img = ImageTk.PhotoImage(Image.open('images/btnCalendar.png'))
    btnCalendar = Button(dateCanvas, bg=menuCanvas.cget('background'), bd=0, highlightthickness=0, image=img, 
                        activebackground=menuCanvas.cget('background'))
    btnCalendar.image = img
    btnCalendar.place(x=175, y=0)
    

    # Crypto Buttons
    btnCanvas = Canvas(menuCanvas, bg=menuCanvas.cget('background'), width=240, height=45, highlightthickness=0)
    menuCanvas.create_window(153, 75, window=btnCanvas)

    btn_ = [
        "images/btnDashAll.png", "images/btnBitcoin.png", 
        "images/btnEthereum.png", "images/btnDogecoin.png"
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
    dashCanvas = Canvas(menuCanvas, bg=menuCanvas.cget('background'), width=1007, height=490, highlightthickness=0)
    menuCanvas.create_window(535, 365, window=dashCanvas)

    img = Image.open("images/Base.png")
    img = img.resize((533, 311), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(img, master=dashCanvas)
    base = Label(dashCanvas, image=test, bg=menuCanvas.cget('background'))
    base.image = test
    base.place(x=0, y=0)

    img = img.resize((533, 154), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(img, master=dashCanvas)
    base1 = Label(dashCanvas, image=test, bg=menuCanvas.cget('background'))
    base1.image = test
    base1.place(x=0, y=332)

    img = Image.open("images/Base1.png")
    img = img.resize((450, 486), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(img, master=dashCanvas)
    base2 = Label(dashCanvas, image=test, bg=menuCanvas.cget('background'))
    base2.image = test
    base2.place(x=553, y=0)


def train():
    # Display Train tab
    menuCanvas.delete('all')
    print('Train')

    menuCanvas.create_text(78, 28, text='TRAIN', font=("Segoe UI bold", 20), fill=color['white'])

    # Cards
    dashCanvas = Canvas(menuCanvas, bg=menuCanvas.cget('background'), width=1007, height=548, highlightthickness=0)
    menuCanvas.create_window(535, 335, window=dashCanvas)

    img = Image.open("images/Base1.png")
    img = img.resize((317, 544), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(img, master=dashCanvas)
    base = Label(dashCanvas, image=test, bg=menuCanvas.cget('background'))
    base.image = test
    base.place(x=0, y=0)

    img = img.resize((665, 544), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(img, master=dashCanvas)
    base1 = Label(dashCanvas, image=test, bg=menuCanvas.cget('background'))
    base1.image = test
    base1.place(x=338, y=0)


def test():
    # Display Test tab
    menuCanvas.delete('all')
    print('Test')

    menuCanvas.create_text(65, 28, text='TEST', font=("Segoe UI bold", 20), fill=color['white'])

    # Cards
    dashCanvas = Canvas(menuCanvas, bg=menuCanvas.cget('background'), width=1007, height=548, highlightthickness=0)
    menuCanvas.create_window(535, 335, window=dashCanvas)

    img = Image.open("images/Base1.png")
    img = img.resize((317, 544), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(img, master=dashCanvas)
    base = Label(dashCanvas, image=test, bg=menuCanvas.cget('background'))
    base.image = test
    base.place(x=0, y=0)

    img = img.resize((665, 544), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(img, master=dashCanvas)
    base1 = Label(dashCanvas, image=test, bg=menuCanvas.cget('background'))
    base1.image = test
    base1.place(x=338, y=0)


def deploy():
    # Display Deploy tab
    menuCanvas.delete('all')
    print('Test')

    menuCanvas.create_text(80, 28, text='DEPLOY', font=("Segoe UI bold", 20), fill=color['white'])

    # Cards
    dashCanvas = Canvas(menuCanvas, bg=menuCanvas.cget('background'), width=1007, height=548, highlightthickness=0)
    menuCanvas.create_window(535, 335, window=dashCanvas)

    img = Image.open("images/Base1.png")
    img = img.resize((1003, 156), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(img, master=dashCanvas)
    base = Label(dashCanvas, image=test, bg=menuCanvas.cget('background'))
    base.image = test
    base.place(x=0, y=0)

    img = img.resize((666, 367), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(img, master=dashCanvas)
    base1 = Label(dashCanvas, image=test, bg=menuCanvas.cget('background'))
    base1.image = test
    base1.place(x=0, y=177)

    img = Image.open("images/Base.png")
    img = img.resize((317, 367), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(img, master=dashCanvas)
    base2 = Label(dashCanvas, image=test, bg=menuCanvas.cget('background'))
    base2.image = test
    base2.place(x=686, y=177)

    
