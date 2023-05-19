from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import pyrebase

config = {
  "apiKey": "AIzaSyAqlITRDZ3gaw5rHhy9hUCwN4xAUDT-svc",
  "authDomain": "epbip-17adb.firebaseapp.com",
  "databaseURL": "https://epbip-17adb-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "epbip-17adb",
  "storageBucket": "epbip-17adb.appspot.com",
  "messagingSenderId": "612338602406",
  "appId": "1:612338602406:web:dd0e8e6d1f905f5d60ff67",
  "measurementId": "G-J1896JVRT9"
}
firebase = pyrebase.initialize_app(config)
database = firebase.database()

# window
login = Tk()
login.title("Login Page")
login.geometry("400x420")


def on_entry(e):
    usernm.configure(show="")
    if usernm.get() == "Email":
        usernm.configure(foreground="black")
        usernm.delete(0, 'end')


def on_password(e):
    if usernm.get() == "":
        usernm.configure(show="", foreground="grey")
        usernm.delete(0, "end")
        usernm.insert(0, "Email")
    else:
        usernm.configure(show="", foreground="black")

def on_enter(e):
    passw.configure(show="*")
    if passw.get() == "Password":
        passw.configure(foreground="black")
        passw.delete(0, "end")


def on_leave(e):
    if passw.get() == "":
        passw.configure(show="", foreground="grey")
        passw.delete(0, "end")
        passw.insert(0, "Password")
    else:
        passw.configure(show="*", foreground="black")
        


def invalid():
    if usernm.get() == 'Email' and passw.get() == 'Password':
        messagebox.showerror("Error", "No input in the field")
    elif usernm.get() == 'Email' or passw.get() == 'Password':
        messagebox.showerror("Error", "No input in other field")
    else:
        users=database.child("Users").get()
        for user in users.each():
            if  usernm.get() != user.val() or passw.get() != user.val():
                messagebox.showerror("Error", "Invalid Email or Password")
            else:
                messagebox.showinfo("Success", "Login successful!")
                login.destroy()
                os.system("Dashboard.py")
             
           

def toreg():
    login.destroy()
    os.system("Registration.py")


def forgot():
    login.destroy()
    os.system("Forgot.py")


# Background
bg_0 = Image.open("img\\bg.jpg")
bck_pk = ImageTk.PhotoImage(bg_0.resize((400, 420)))

lbl = Label(login, image=bck_pk, border=0)
lbl.place(x=0, y=0, relwidth=1, relheight=1)
lbl.pack()

# logo
box_2 = Frame(login, width=300, height=320, bg='#010F57')
box_2.place(x=50, y=50)

logo = Image.open("img\\logoo.png")
log_pk = ImageTk.PhotoImage(logo.resize((105, 100)))

lbl = Label(box_2, image=log_pk, border=0)
lbl.place(x=100, y=5)

log_name = Label(box_2, text='E.P.B.I.P', fg='white', bg='#010F57', font=('Copperplate', 18, 'bold'))
log_name.place(x=100, y=100)

# user
usernm = Entry(box_2, width=25, fg='grey', border=1, bg='white', font=('Arial', 11, 'bold'), show="")
usernm.place(x=50, y=140)
usernm.insert(0, 'Email')
usernm.bind('<FocusIn>', on_entry)
usernm.bind('<FocusOut>', on_password)

# password
passw = Entry(box_2, width=25, fg='grey', border=1, bg='white', font=('Arial', 11, 'bold'),show="")
passw.place(x=50, y=175)
passw.insert(0, 'Password')
passw.bind('<FocusIn>', on_enter)
passw.bind('<FocusOut>', on_leave)

# button
Button(box_2, width=10, pady=5, text="Log In", bg='white', cursor='hand2', font=('Arial', 12, 'bold'),
       command=invalid).place(x=100, y=215)

# forgot password
f_pass = Button(box_2, width=15, text='Forgot Password?', border=0, bg='#010F57', cursor='hand2', fg='#38B6FF',
                font=('Arial', 9, 'bold', 'underline'), command=forgot)
f_pass.place(x=100, y=265)

# To Register
to_reg = Label(box_2, text="Don't have an account?", fg='white', bg='#010F57', font=('Arial', 9, 'bold'))
to_reg.place(x=60, y=295)

sign_up = Button(box_2, width=6, text='Sign up', border=0, bg='#010F57', cursor='hand2', fg='#38B6FF',
                 font=('Arial', 9, 'bold', 'underline'), command=toreg)
sign_up.place(x=195, y=295)

login.mainloop()
