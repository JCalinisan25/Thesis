from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os, re, pyrebase, json

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
login = Tk()
login.title("Login Page")
login.geometry("400x420")

# Email validation
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

# Email
def on_entry(e):
    if usernm.get() == "Example@email.com":
        usernm.configure(foreground="black")
        usernm.delete(0, 'end')

def on_password(e):
    if usernm.get() == "":
        usernm.insert(0, 'Example@email.com')
        usernm.configure(foreground="grey")

# Password
def on_enter(e):
    passw.configure(show="*")
    if passw.get() == "Password":
        passw.configure(foreground="black")
        passw.delete(0, "end")

def on_leave(e):
    if passw.get() == "":
        passw.configure(show="")
        passw.insert(0, 'Password')
        passw.configure(foreground="grey")

# Password Visibility Toggle
def show_pass():
    passw["show"] = ""
    hid_button = Button(box_2, width=15, height=15, bg='white', bd=0, image=hide_pk, command=hide_pass)
    hid_button.place(x=235, y=177)

def hide_pass():
    passw["show"] = "*"
    show_button = Button(box_2, width=15, height=15, bg='white', bd=0, image=show_pk, command=show_pass)
    show_button.place(x=235, y=177)

def invalid():
    if usernm.get() == 'Example@email.com' and passw.get() == 'Password':
        messagebox.showerror("Error", "No input in the field")
    elif usernm.get() == 'Example@email.com' or passw.get() == 'Password':
        messagebox.showerror("Error", "One of the fields is empty")
    else:
        email = usernm.get()
        password = passw.get()
        if not is_valid_email(email):
            messagebox.showerror("Error", "Invalid Email Format!")
        else:
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                # save the user's email after a successful login
                with open('user.json', 'w') as file:
                    json.dump({'email': email}, file)
                messagebox.showinfo("Success", "Login Successfully")
                login.destroy()
                os.system("Dashboard.py")
            except:
                messagebox.showerror("Error", "Invalid Username or Password")


#To registration
def toreg():
    login.destroy()
    os.system("Registration.py")

#To forgot password
def forgot():
    login.destroy()
    os.system("Forgot.py")

def remove_focus(e):
    login.focus()

# Background
bg_0 = Image.open("img\\bg.jpg")
bck_pk = ImageTk.PhotoImage(bg_0.resize((400, 420)))

lbl = Label(login, image=bck_pk, border=0)
lbl.place(x=0, y=0, relwidth=1, relheight=1)
lbl.pack()

# Logo
box_2 = Frame(login, width=300, height=320, bg='#010F57')
box_2.place(x=50, y=50)

logo = Image.open("img\\logoo.png")
log_pk = ImageTk.PhotoImage(logo.resize((105, 100)))

lbl = Label(box_2, image=log_pk, border=0)
lbl.place(x=100, y=5)

log_name = Label(box_2, text='E.P.B.I.P', fg='white', bg='#010F57', font=('Copperplate', 18, 'bold'))
log_name.place(x=100, y=100)

# User
usernm = Entry(box_2, width=25, fg='grey', border=1, bg='white', font=('Arial', 11, 'bold'), show="")
usernm.place(x=50, y=140)
usernm.insert(0, 'Example@email.com')
usernm.bind('<FocusIn>', on_entry)
usernm.bind('<FocusOut>', on_password)
usernm.bind('<Button-1>', remove_focus)

# Password
passw = Entry(box_2, width=25, fg='grey', border=1, bg='white', font=('Arial', 11, 'bold'), show="")
passw.place(x=50, y=175)
passw.insert(0, 'Password')
passw.bind('<FocusIn>', on_enter)
passw.bind('<FocusOut>', on_leave)
passw.bind('<Button-1>', remove_focus)

# Password Visibility Toggle Button
show = Image.open("img\\show.jpg")
show_pk = ImageTk.PhotoImage(show.resize((15, 12)))
hide = Image.open("img\\hide.jpg")
hide_pk = ImageTk.PhotoImage(hide.resize((15, 12)))
vis_button = Button(box_2, width=18, height=17, bg='white', bd=0, image=show_pk, command=show_pass)
vis_button.place(x=234, y=177)

# Button
Button(box_2, width=10, pady=5, text="Log In", bg='white', cursor='hand2', font=('Arial', 12, 'bold'),
       command=invalid).place(x=100, y=215)

# Forgot password
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
