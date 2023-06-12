from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os, re, pyrebase, json

# Access the Realtime Database and retrieve data
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
login.title("E.P.B.I.P")
login.geometry("700x400")
login.resizable(False, False)
login.iconbitmap(r'img\\logo.ico')


# Set the position of the terminal window
def center_window(window):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 3
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Center the tkinter window
center_window(login)

# Email validation
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

# Email
def on_entry(e):
    if usernm.get() == "Example@email.com":
        usernm.configure(foreground="#010F57")
        usernm.delete(0, 'end')

def on_password(e):
    if usernm.get() == "":
        usernm.insert(0, 'Example@email.com')
        usernm.configure(foreground="#9098ba")

# Password
def on_enter(e):
    passw.configure(show="*")
    if passw.get() == "Password":
        passw.configure(foreground="#010F57")
        passw.delete(0, "end")

def on_leave(e):
    if passw.get() == "":
        passw.configure(show="")
        passw.insert(0, 'Password')
        passw.configure(foreground="#9098ba")

# Password Visibility Toggle
def show_pass():
    passw["show"] = ""
    hid_button = Button(box_2, width=15, height=15, bg='white', bd=0, image=hide_pk, command=hide_pass)
    hid_button.place(x=232, y=175)

def hide_pass():
    passw["show"] = "*"
    show_button = Button(box_2, width=15, height=15, bg='white', bd=0, image=show_pk, command=show_pass)
    show_button.place(x=232, y=175)

def invalid():
    email = usernm.get()
    password = passw.get()
    if email == 'Example@email.com' and password == 'Password':
        messagebox.showerror("Error", "Please enter your email and password.")
    elif email == 'Example@email.com' or email == '':
        messagebox.showerror("Error", "Please enter your email address.")
    elif not is_valid_email(email):
            messagebox.showerror("Error", "Invalid Email Format!")
    elif password == 'Password' or password == '':
        messagebox.showerror("Error", "Please enter your password")
    else:
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            # save the user's email after a successful login
            with open('user.json', 'w') as file:
                json.dump({'email': email}, file)
            login.destroy()
            os.system("Dashboard.py")
        except:
            messagebox.showerror("Error", "Invalid Email or Password!")
    # email = "danielmarco@gmail.com"
    # password = "Danielmarco1!"
    # main()


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
bg_0 = Image.open("img\\bg8.jpg")
bck_pk = ImageTk.PhotoImage(bg_0.resize((700, 400)))

lbl = Label(login, image=bck_pk, border=0)
lbl.place(x=0, y=0, relwidth=1, relheight=1)
lbl.pack()

# Logo
box_2 =Frame(login, width=300, height=350, bg='white')
box_2.place(x=50, y=25)

box_3 =Frame(login, width=300, height=350, bg='#010F57')
box_3.place(x=350, y=25)

log = Image.open("img\\log.png")
log_pk = ImageTk.PhotoImage(log.resize((320, 320)))

lbl = Label(box_3, image=log_pk, border=0, bg='#010F57')
lbl.place(x=0, y=20)

log_name = Label(box_2, text='Sign In', fg='#021976', bg='White', font=('Copperplate', 18, 'bold'))
log_name.place(x=100, y=40)

# User
usernm = Entry(box_2, width=25, fg='#9098ba', border=0, bg='white', font=('Arial', 11, 'bold') )
usernm.place(x=50, y=125)
usernm.insert(0, 'Example@email.com')
usernm.bind('<FocusIn>', on_entry)
usernm.bind('<FocusOut>', on_password)
usernm.bind('<Button-1>', remove_focus)
Frame(box_2, width=205, height=2, bg='#010F57').place(x=48, y=145)

# Password
passw = Entry(box_2, width=22, fg='#9098ba', border=0, bg='white', font=('Arial', 11, 'bold'))
passw.place(x=50, y=175)
passw.insert(0, 'Password')
passw.bind('<FocusIn>', on_enter)
passw.bind('<FocusOut>', on_leave)
passw.bind('<Button-1>', remove_focus)
Frame(box_2, width=205, height=2, bg='#010F57').place(x=48, y=195)

# Password Visibility Toggle Button
show = Image.open("img\\show.jpg")
show_pk = ImageTk.PhotoImage(show.resize((15, 12)))
hide = Image.open("img\\hide.jpg")
hide_pk = ImageTk.PhotoImage(hide.resize((15, 12)))
vis_button = Button(box_2, width=15, height=15, bg='white', bd=0, image=show_pk, command=show_pass)
vis_button.place(x=232, y=175)

# Button
Button(box_2, width=20, pady=5, text="Sign In", bg='#041D9B', fg='white', cursor='hand2', font=('Arial', 12, 'bold'),
       command=invalid, bd=0, activebackground='#021976', activeforeground='white').place(x=48, y=245)

# Forgot password
f_pass = Button(box_2, width=15, text='Forgot Password?', border=0, bg='white', cursor='hand2', fg='#021976',
                font=('Arial', 9), command=forgot, activeforeground='#A13CA6', activebackground='white')
f_pass.place(x=45, y=205)

# To Register
to_reg = Label(box_2, text="Don't have an account?", fg='#021976', bg='white', font=('Arial', 9))
to_reg.place(x=60, y=295)

sign_up = Button(box_2, width=6, text='Sign up', border=0, bg='white', cursor='hand2', fg='#021976',
                 font=('Arial', 9, 'bold', 'underline'), command=toreg, activeforeground='#A13CA6',
                 activebackground='white')
sign_up.place(x=195, y=295)

login.mainloop()
