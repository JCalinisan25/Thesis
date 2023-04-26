from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# window
login = Tk()
login.title("Login Page")
login.geometry("400x420")


def on_entry(e):
    user.delete(0, 'end')


def on_password(e):
    name = user.get()
    if name == '':
        user.insert(0, 'Username or Email')


def on_enter(e):
    passw.delete(0, 'end')


def on_leave(e):
    name = passw.get()
    if name == '':
        passw.insert(0, 'Password')


def invalid():
    if user.get() == 'Username or Email' and passw.get() == 'Password':
        messagebox.showerror("Error", "No Username or Password Input!")
    elif user.get() == 'Username or Email' or passw.get() == '' and user.get() == '' or passw.get() == 'Password':
        messagebox.showerror("Error", "Invalid Username or Password!")
    else:
        login.destroy()
        os.system("Dashboard.py")


def toreg():
    login.destroy()
    os.system("Registration.py")


def forgot():
    login.destroy()
    os.system("Forgot.py")


# Background
bg_0 = Image.open("D:\\Codes\\Python\\Thesis\\img\\bg.jpg")
bck_pk = ImageTk.PhotoImage(bg_0.resize((400, 420)))

lbl = Label(login, image=bck_pk, border=0)
lbl.place(x=1, y=1)


# Header
box_1 = Frame(login, width=400, height=55, bg='#010F57')
box_1.place(x=3, y=5)
heading = Label(login, text='SIGN IN', fg='white', bg='#010F57', font=('Arial', 30, 'bold'))
heading.place(x=130, y=5)

# logo
box_2 = Frame(login, width=300, height=320, bg='#010F57')
box_2.place(x=50, y=80)

logo = Image.open("D:\\Codes\\Python\\Thesis\\img\\logoo.png")
log_pk = ImageTk.PhotoImage(logo.resize((105, 100)))

lbl = Label(box_2, image=log_pk, border=0)
lbl.place(x=100, y=5)

log_name = Label(box_2, text='E.P.B.I.P', fg='white', bg='#010F57', font=('Copperplate', 18, 'bold'))
log_name.place(x=100, y=100)

# user
user = Entry(box_2, width=25, fg='grey', border=1, bg='white', font=('Arial', 11, 'bold'))
user.place(x=50, y=140)
user.insert(0, 'Username or Email')
user.bind('<FocusIn>', on_entry)
user.bind('<FocusOut>', on_password)

# password
passw = Entry(box_2, width=25, fg='black', border=1, bg='white', font=('Arial', 11, 'bold'), show='*')
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
