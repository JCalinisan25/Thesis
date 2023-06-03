from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import os, pyrebase, json

config = {
'apiKey': "AIzaSyAqlITRDZ3gaw5rHhy9hUCwN4xAUDT-svc",
'authDomain': "epbip-17adb.firebaseapp.com",
'databaseURL': "https://epbip-17adb-default-rtdb.asia-southeast1.firebasedatabase.app",
'projectId': "epbip-17adb",
'storageBucket': "epbip-17adb.appspot.com",
'messagingSenderId': "612338602406",
'appId': "1:612338602406:web:dd0e8e6d1f905f5d60ff67",
'measurementId': "G-J1896JVRT9"
}
firebase = pyrebase.initialize_app(config)
database = firebase.database()

# window
dash = Tk()
dash.title("E.P.B.I.P")
dash.geometry("450x450")
dash.resizable(False, False)
dash.iconbitmap(r'img\\logo.ico')

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
bg_0 = Image.open("img\\bg8.jpg")
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

person = Image.open("img\\person.JPG")
per_pk = ImageTk.PhotoImage(person.resize((95, 100)))

lbl = Label(box_2, image=per_pk, border=0)
lbl.place(x=20, y=5)

edit = Image.open("img\\edit.PNG")
ed_pk = ImageTk.PhotoImage(edit.resize((18, 18)))

lbl = Label(box_2, image=ed_pk, border=0)
lbl.place(x=15, y=110)

# Get the email from the login process
try:
    with open('user.json', 'r') as file:
        user_info = json.load(file)
        email = user_info['email']
except FileNotFoundError:
    messagebox.showerror("Error", "No user is signed in!")
    email = ""
    

# Retrieve username from Firebase Realtime Database based on the email
users = database.child("Users").get()
username = "username"
for user in users.each():
    if user.val()['email'] == email:
        username = user.val()['username']
        break

username_label_text = f"Hi, {username}"
user = Label(box_2, text=username_label_text, fg='white', bg='#010F57', font=('Arial', 11, 'bold'))
user.place(x=30, y=110)

# logout
log = Image.open("img\\logout.JPG")
lg_pk = ImageTk.PhotoImage(log.resize((30, 25)))

lbl = Label( image=lg_pk)

lg_btn = Button(box_2, bg="#010F57", bd=0, height=40, width=30, image=lg_pk, cursor='hand2', command=tosign)
lg_btn.place(x=350, y=1)

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
