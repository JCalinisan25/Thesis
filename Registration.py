from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import pyrebase, json, requests, webbrowser
import os, re

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
auth = firebase.auth()

# Window
regist = Tk()
regist.title("E.P.B.I.P")
regist.geometry("700x400")
regist.resizable(False, False)
regist.iconbitmap(r'img\\logo.ico')

# Back to login page
def to_sign():
    regist.destroy()
    os.system('Login.py')

# Show password
def show_password():
    if passw.cget('show') == '*':
        passw.config(show='')
    else:
        passw.config(show='*')

def is_valid_email(email):
    # Use regex pattern for email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

# Validation of username and password
def validate_inputs():
    global email
    email_value = email.get()
    password = passw.get()
    c_password = c_passw.get()

    if usernm.get() == '' and email.get() == '' and password == '' and c_password == '':
        messagebox.showerror("Error", "No input in the field!")
    elif usernm.get() == '' or email.get() == '' or password == '' or c_password =='':
        messagebox.showerror("Error", "No input in other field!")
    elif not re.match(r"^(?=.*\d)(?=.*[A-Z])(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", password):
        messagebox.showerror("Error", "Password must meet the following criteria:\n"
                             "• Must be at least 8 characters long\n"
                             "• At least one digit\n"
                             "• At least one uppercase letter\n"
                             "• At least one punctuation mark.")
    elif password != c_password:
        messagebox.showerror("Error", "Passwords do not match!")
    elif not is_valid_email(email_value):
        messagebox.showerror("Error", "Invalid Email Address Format!\n(Example: Abcd@email.com)")
    elif not checks.get():
        messagebox.showerror("Error", "Please accept the terms and conditions!")
    else:
        try:
            user = auth.create_user_with_email_and_password(email_value, password)
        except requests.exceptions.HTTPError as error:
            error_json = error.args[1]
            error_details = json.loads(error_json)['error']['message']
            if error_details == 'EMAIL_EXISTS':
                messagebox.showerror("Error", "This email address is already in exist!")
                return
            else:
                messagebox.showerror("Error", error_details)
                return

        auth.send_email_verification(user['idToken'])
        data = {
            "username": usernm.get(),
            "email": email_value
        }
        database.child("Users").push(data)
        messagebox.showinfo("Success", "Data saved successfully!")
        regist.destroy()
        os.system('verified.py')

# PDF Terms and Conditions 
def show_terms():
    pdf_file = "Terms_and_Conditions.pdf"
    webbrowser.open(pdf_file)

# PDF Data Privacy Policy
def show_policy():
    pdf_file = "Data_Privacy_Policy.pdf"
    webbrowser.open(pdf_file)

# Password Visibility Toggle for password
def show_pass():
    passw["show"] = ""
    hid_button = Button(box_2, width=17, height=16, bg='white', bd=0, image=hide_pk, command=hide_pass)
    hid_button.place(x=214, y=171)

def hide_pass():
    passw["show"] = "*"
    show_button = Button(box_2, width=17, height=16, bg='white', bd=0, image=show_pk, command=show_pass)
    show_button.place(x=214, y=171)

# Password Visibility Toggle for confirm password
def cshow_pass():
    c_passw["show"] = ""
    chid_button = Button(box_2, width=17, height=16, bg='white', bd=0, image=chide_pk, command=chide_pass)
    chid_button.place(x=214, y=221)

def chide_pass():
    c_passw["show"] = "*"
    cshow_button = Button(box_2, width=17, height=16, bg='white', bd=0, image=cshow_pk, command=cshow_pass)
    cshow_button.place(x=214, y=221)

def update_password_strength():
    password = passw.get()
    strength_label.config(fg='white')  # Reset the color to white

    if len(password) == 0:
        strength_label.place_forget()  # Hide the strength label
    else:
        strength_label.place(x=90, y=150)  # Show the strength label

        # Define regular expressions for different password strength levels
        strong_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        medium_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{6,}$"

        # Check password strength using the regular expressions
        if re.match(strong_regex, password):
            strength_label.config(text="Strong Password", fg="green")
        elif re.match(medium_regex, password):
            strength_label.config(text="Medium Password", fg="orange")
        else:
            strength_label.config(text="Weak Password", fg="red")

def get_password_strength(password):
    if len(password) < 8:
        return "Weak"
    elif re.search(r'[A-Z]', password) is None or re.search(r'[a-z]', password) is None or re.search(r'\d', password) is None:
        return "Medium"
    else:
        return "Strong"

# Background
bg_0 = Image.open("img\\bg8.jpg")
bck_pk = ImageTk.PhotoImage(bg_0.resize((700, 400)))

lbl = Label(regist, image=bck_pk, border=0)
lbl.place(x=1, y=1)

# Logo
box_2 = Frame(regist, width=300, height=360, bg='#010F57')
box_2.place(x=350, y=20)

box_3 = Frame(regist, width=300, height=360, bg='white')
box_3.place(x=50, y=20)

log_name = Label(box_2, text='Register', fg='White', bg='#010F57', font=('Arial', 18, 'bold'))
log_name.place(x=100, y=10)

log = Image.open("img\\reg.jpg")
log_pk = ImageTk.PhotoImage(log.resize((320, 320)))

lbl = Label(box_3, image=log_pk, border=0, bg='#010F57')
lbl.place(x=0, y=20)

username = StringVar()
emails = StringVar()
password = StringVar()
c_password = StringVar()

# User
user_name = Label(box_2, text='Username:', fg='white', bg='#010F57', font=('Arial', 9, 'bold'))
user_name.place(x=20, y=100)
usernm = Entry(box_2, textvariable=username, width=30, fg='black', border=1, bg='white', font=('Arial', 10, 'bold'))
usernm.place(x=20, y=120)

# Email
email_name = Label(box_2, text='Email:', fg='white', bg='#010F57', font=('Arial', 9, 'bold'))
email_name.place(x=20, y=50)
email = Entry(box_2, textvariable=emails, width=30, fg='black', border=1, bg='white', font=('Arial', 10, 'bold'))
email.place(x=20, y=70)

# Password
pass_name = Label(box_2, text='Password:', fg='white', bg='#010F57', font=('Arial', 9, 'bold'))
pass_name.place(x=20, y=150)
passw = Entry(box_2, textvariable=password, width=30, fg='black', border=1, bg='white', font=('Arial', 10, 'bold'),
              show="*")
passw.place(x=20, y=170)
passw.bind("<KeyRelease>", lambda event: update_password_strength())

#Confirm Password
c_pass = Label(box_2, text='Confirm Password:', fg='white', bg='#010F57', font=('Arial', 9, 'bold'))
c_pass.place(x=20, y=200)
c_passw = Entry(box_2, textvariable=c_password, width=30, fg='black', border=1, bg='white', font=('Arial', 10, 'bold'),
              show="*")
c_passw.place(x=20, y=220)

# Show password
# Password Visibility Toggle Button
show = Image.open("img\\show.jpg")
show_pk = ImageTk.PhotoImage(show.resize((15, 12)))
hide = Image.open("img\\hide.jpg")
hide_pk = ImageTk.PhotoImage(hide.resize((15, 12)))
vis_button = Button(box_2, width=17, height=16, bg='white', bd=0, image=show_pk, command=show_pass)
vis_button.place(x=214, y=171)

chow = Image.open("img\\show.jpg")
cshow_pk = ImageTk.PhotoImage(show.resize((15, 12)))
chide = Image.open("img\\hide.jpg")
chide_pk = ImageTk.PhotoImage(hide.resize((15, 12)))
cvis_button = Button(box_2, width=17, height=16, bg='white', bd=0, image=cshow_pk, command=cshow_pass)
cvis_button.place(x=214, y=221)

# Create the password strength indicator label
strength_label = Label(box_2, text="", font=('Arial', 8, 'bold'), bg='#010F57')
strength_label.place_forget()

# Button
reg = Button(box_2, width=10, pady=5, text="Register", bg='white', cursor='hand2', font=('Arial', 12, 'bold'),
             command=validate_inputs)
reg.place(x=20, y=305)

log = Button(box_2, width=10, pady=5, text="Login", bg='white', cursor='hand2', font=('Arial', 12, 'bold'),
             command=to_sign)
log.place(x=150, y=305)


# Terms and Conditions/DPA Acceptance
checks = BooleanVar()

checks_button = Checkbutton(regist, variable=checks, onvalue=True, offvalue=False, bg='#010F57', bd=0)
checks_button.place(x=365, y=271)

text2 = Label(box_2, text="I agree to E.P.B.I.P", fg='white', bg='#010F57', font=('Arial', 8, 'bold'))
text2.place(x=37, y=252)

trm = Button(box_2, width=17, text='terms and conditions', border=0, bg='#010F57', cursor='hand2', fg='#38B6FF',
             font=('Arial', 8, 'bold', 'underline'), command=show_terms)
trm.place(x=137, y=252)

text3 = Label(box_2, text="and ", fg='white', bg='#010F57', font=('Arial', 8, 'bold'))
text3.place(x=37, y=272)

dpa = Button(box_2, width=10, text='Privacy Policy', border=0, bg='#010F57', cursor='hand2', fg='#38B6FF',
             font=('Arial', 8, 'bold', 'underline'), command=show_policy)
dpa.place(x=62, y=272)

regist.mainloop()
