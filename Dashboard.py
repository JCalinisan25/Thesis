from tkinter import *
from PIL import Image, ImageTk
import os

# window
dash = Tk()
dash.title("Dashboard")
dash.geometry("450x450")


def tosign():
    dash.destroy()
    os.system('Login.py')


def toresult():
    dash.destroy()
    os.system('Results.py')


def toscan():
    dash.destroy()
    os.system('scan.py')


# Background
bg_0 = Image.open("img\\bg.jpg")
bck_pk = ImageTk.PhotoImage(bg_0.resize((450, 450)))

lbl = Label(dash, image=bck_pk, border=0)
lbl.place(x=1, y=1)

# Header
box_1 = Frame(dash, width=500, height=55, bg='#010F57')
box_1.place(x=3, y=5)
heading = Label(dash, text='DASHBOARD', fg='white', bg='#010F57', font=('Arial', 30, 'bold'))
heading.place(x=100, y=5)

# profile
box_2 = Frame(dash, width=390, height=355, bg='#010F57')
box_2.place(x=30, y=80)

person = Image.open("D:\\Codes\\Python\\Thesis\\img\\person.JPG")
per_pk = ImageTk.PhotoImage(person.resize((105, 110)))

lbl = Label(box_2, image=per_pk, border=0)
lbl.place(x=20, y=5)

edit = Image.open("img\\edit.PNG")
ed_pk = ImageTk.PhotoImage(edit.resize((18, 18)))

lbl = Label(box_2, image=ed_pk, border=0)
lbl.place(x=15, y=110)

user = Label(box_2, text='Username', fg='white', bg='#010F57', font=('Arial', 11, 'bold'))
user.place(x=30, y=110)

# logout
log = Image.open("img\\logout.JPG")
lg_pk = ImageTk.PhotoImage(log.resize((30, 25)))

lbl = Label(dash, image=lg_pk, border=0)
lbl.place(x=300, y=91)

lg_btn = Button(box_2, bg="#010F57", bd=0, height=1, width=9, text="   Logout", fg='white', font=('Arial', 15, 'bold'),
                cursor='hand2', command=tosign)
lg_btn.place(x=270, y=5)

# To scan
scan_btn = PhotoImage(file='img\scan.png')
sc_label = Label(image=scan_btn)

sc_btn = Button(box_2, image=scan_btn, width=290, height=90, bg="#021976", bd=0, cursor='hand2', command=toscan)
sc_btn.place(x=50, y=145)

# To results
rep_btn = PhotoImage(file="img\det.png")
rp_label = Label(image=rep_btn)

rp_btn = Button(box_2, image=rep_btn, width=290, height=90, bg="#021976", bd=0, cursor='hand2', command=toresult)
rp_btn.place(x=50, y=250)

dash.mainloop()
