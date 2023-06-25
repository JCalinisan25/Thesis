import os
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import pyrebase, requests, json

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
forgot.title("E.P.B.I.P")
forgot.geometry("400x400")
forgot.resizable(False, False)
forgot.iconbitmap(r'img\\logo.ico')

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
center_window(forgot)

def on_in(e):
    if f_pass.get() == "Example@email.com":
        f_pass.delete(0, 'end')
        f_pass.configure(foreground="black")


def on_out(e):
    if f_pass.get() == "":
        f_pass.insert(0, "Example@email.com")
        f_pass.configure(foreground="grey")



def log():
    forgot.destroy()
    os.system("Login.py")

def remove_focus(e):
    forgot.focus()

# Function to reset password
def reset_password():
    email = f_pass.get()
    if email == "Example@email.com" or email == "":
        messagebox.showerror("Error", "Please enter your email.")
    else:

        try:
            auth.send_password_reset_email(email)
            messagebox.showinfo("Success", "Password reset request has been sent successfully.")
            forgot.destroy()
            os.system("Login.py")
        except requests.exceptions.HTTPError as e:
            error_json = e.args[0].response.text
            error_message = json.loads(error_json)['error']['message']
        
            if error_message == 'EMAIL_NOT_FOUND':
                messagebox.showerror("Error", "Email is not registered!")
            else:
                messagebox.showerror("Error", "Invalid Email Address!")

# Background
bg_0 = Image.open("img\\bg8.jpg")
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
log_name.place(x=130, y=90)

# Content
box_2 = Frame(box_1, width=450, height=3, bg='white')
box_2.place(x=1, y=120)

heading = Label(box_1, text='Forgot your password?', fg='white', bg='#010F57', font=('Arial', 16, 'bold'))
heading.place(x=2, y=125)

info = Label(box_1, text="Please enter your email to reset your password.", fg='white',
             bg='#010F57', font=('Arial', 11, 'bold'))
info.place(x=10, y=160)

f_pass = Entry(box_1, width=35, fg='grey', border=1, bg='white', font=('Arial', 12, 'bold'), show="")
f_pass.place(x=27, y=210)
f_pass.insert(0, 'Example@email.com')
f_pass.bind('<FocusIn>', on_in)
f_pass.bind('<FocusOut>', on_out)
f_pass.bind('<Button-1>', remove_focus)

# button
btn1 = Button(box_1, width=15, pady=5, text="Reset Password", bg='white', fg='black', cursor='hand2', border=0,
              font=('Arial', 12, 'bold'), command=reset_password)
btn1.place(x=110, y=250)

btn2 = Button(box_1, width=15, pady=5, text="Cancel", bg='white', fg='black', cursor='hand2', border=0,
              font=('Arial', 12, 'bold'), command=log)
btn2.place(x=110, y=300)

forgot.mainloop()