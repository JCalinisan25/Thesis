import os
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import pyrebase

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
auth = firebase.auth()

# window
forgot = Tk()
forgot.title("Forgot Password Page")
forgot.geometry("400x400")


def on_in(e):
    if f_pass.get() == "Enter Email":
        f_pass.delete(0, 'end')
        f_pass.configure(foreground="black")


def on_out(e):
    if f_pass.get() == "":
        f_pass.insert(0, "Enter Email")
        f_pass.configure(foreground="grey")



def log():
    forgot.destroy()
    os.system("Login.py")

def reset_password():
    email = f_pass.get()
    try:
        # Attempt to send the password reset email.
        auth.send_password_reset_email(email)
        messagebox.showinfo("Success", "Password reset has been sent to your email address!")
        forgot.destroy()
        os.system('Login.py')
    except:
        messagebox.showerror("Error", "Failed to send reset password email")

# Background
bg_0 = Image.open("img\\bg.jpg")
bck_pk = ImageTk.PhotoImage(bg_0.resize((400, 400)))

lbl = Label(forgot, image=bck_pk, border=0)
lbl.place(x=1, y=1)

# box
box_1 = Frame(forgot, width=370, height=360, bg='#010F57')
box_1.place(x=15, y=20)

# logo
logo = Image.open("img\\logoo.png")
log_pk = ImageTk.PhotoImage(logo.resize((95, 90)))

lbl = Label(box_1, image=log_pk, border=0)
lbl.place(x=150, y=2)

log_name = Label(box_1, text='E.P.B.I.P', fg='white', bg='#010F57', font=('Copperplate', 18, 'bold'))
log_name.place(x=145, y=90)

# Content
box_2 = Frame(box_1, width=450, height=3, bg='white')
box_2.place(x=1, y=120)

heading = Label(box_1, text='Trouble Logging In?', fg='white', bg='#010F57', font=('Arial', 16, 'bold'))
heading.place(x=5, y=125)

info = Label(box_1, text="Please enter your email to send link \nto get back into your account.", fg='white',
             bg='#010F57', font=('Arial', 11, 'bold'))
info.place(x=60, y=160)

f_pass = Entry(box_1, width=35, fg='grey', border=1, bg='white', font=('Arial', 12, 'bold'), show="")
f_pass.place(x=27, y=210)
f_pass.insert(0, 'Enter Email')
f_pass.bind('<FocusIn>', on_in)
f_pass.bind('<FocusOut>', on_out)

# button
btn1 = Button(box_1, width=15, pady=5, text="Send Login Link", bg='white', fg='black', cursor='hand2', border=0,
              font=('Arial', 12, 'bold'), command=reset_password)
btn1.place(x=110, y=250)

btn2 = Button(box_1, width=15, pady=5, text="Cancel", bg='white', fg='black', cursor='hand2', border=0,
              font=('Arial', 12, 'bold'), command=log)
btn2.place(x=110, y=300)

forgot.mainloop()
