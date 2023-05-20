from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import firebase_admin
from firebase_admin import credentials, db
import webbrowser
import os
import re

cred = credentials.Certificate('credential.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://epbip-17adb-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

database_ref = db.reference('Users')

# Window
regist = Tk()
regist.title("Registration Page")
regist.geometry("700x400")

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

    if usernm.get() == '' and email.get() == '' and password == '':
        messagebox.showerror("Error", "No input in the field!")
    elif usernm.get() == '' or email.get() == '' or password == '':
        messagebox.showerror("Error", "No input in other field!")
    elif not re.match(r"^(?=.*\d)(?=.*[A-Z])(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", password):
        messagebox.showerror("Error", "Password must meet the following criteria:\n"
                             "• Must be at least 8 characters long\n"
                             "• At least one digit\n"
                             "• At least one uppercase letter\n"
                             "• At least one punctuation mark.")
    elif not is_valid_email(email_value):
        messagebox.showerror("Error", "Invalid email address!\n\n(Example: Abcd@example.com)")
    elif not checks.get():
        messagebox.showerror("Error", "Please accept the terms and conditions!")
    else:
        email = email.get()
        if check_user_exist(email):
            messagebox.showerror("Error", "User already exists!")
        else:
            data = {
                "username": usernm.get(),
                "email": email,
                "password": passw.get()
            }
            new_user_ref = database_ref.push()
            new_user_ref.set(data)
            messagebox.showinfo("Success", "Data saved successfully!")
            regist.destroy()
            os.system('EmailVerif.py')


# Check if the user already exists
def check_user_exist(email):
    data = database_ref.get()
    for user_key, user_data in data.items():
        if 'email' in user_data and user_data['email'] == email:
            return True
    return False

# PDF Terms and Conditions
def show_terms():
    pdf_file = "Terms_and_Conditions.pdf"
    webbrowser.open(pdf_file)

# Password Visibility Toggle
def show_pass():
    passw["show"] = ""
    hid_button = Button(box_2, width=15, height=15, bg='white', bd=0, image=hide_pk, command=hide_pass)
    hid_button.place(x=515, y=126)

def hide_pass():
    passw["show"] = "*"
    show_button = Button(box_2, width=15, height=15, bg='white', bd=0, image=show_pk, command=show_pass)
    show_button.place(x=515, y=126)

def update_password_strength():
    password = passw.get()
    strength_label.config(fg='white')  # Reset the color to white

    if len(password) == 0:
        strength_label.place_forget()  # Hide the strength label
    else:
        strength_label.place(x=360, y=152)  # Show the strength label

        # Define regular expressions for different password strength levels
        strong_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        medium_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{6,}$"

        # Check password strength using the regular expressions
        if re.match(strong_regex, password):
            strength_label.config(text="Password Strength: Strong", fg="green")
        elif re.match(medium_regex, password):
            strength_label.config(text="Password Strength: Medium", fg="orange")
        else:
            strength_label.config(text="Password Strength: Weak", fg="red")

def get_password_strength(password):
    if len(password) < 8:
        return "Weak"
    elif re.search(r'[A-Z]', password) is None or re.search(r'[a-z]', password) is None or re.search(r'\d', password) is None:
        return "Medium"
    else:
        return "Strong"

# Background
bg_0 = Image.open("img\\bg.jpg")
bck_pk = ImageTk.PhotoImage(bg_0.resize((700, 400)))

lbl = Label(regist, image=bck_pk, border=0)
lbl.place(x=1, y=1)

# Header
box_1 = Frame(regist, width=700, height=55, bg='#010F57')
box_1.place(x=3, y=5)
heading = Label(regist, text='REGISTER', fg='white', bg='#010F57', font=('Arial', 30, 'bold'))
heading.place(x=250, y=5)

# Logo
box_2 = Frame(regist, width=555, height=290, bg='#010F57')
box_2.place(x=70, y=80)

logo = Image.open("img\\logoo.png")
log_pk = ImageTk.PhotoImage(logo.resize((210, 205)))

lbl = Label(box_2, image=log_pk, border=0)
lbl.place(x=5, y=15)

log_name = Label(box_2, text='E.P.B.I.P', fg='white', bg='#010F57', font=('Copperplate', 30, 'bold'))
log_name.place(x=30, y=220)

username = StringVar()
emails = StringVar()
password = StringVar()

# User
user_name = Label(box_2, text='Username:', fg='white', bg='#010F57', font=('Arial', 17, 'bold'))
user_name.place(x=225, y=23)
usernm = Entry(box_2, textvariable=username, width=23, fg='black', border=1, bg='white', font=('Arial', 11, 'bold'))
usernm.place(x=350, y=27)

# Email
email_name = Label(box_2, text='Email Add.:', fg='white', bg='#010F57', font=('Arial', 18, 'bold'))
email_name.place(x=212, y=70)
email = Entry(box_2, textvariable=emails, width=23, fg='black', border=1, bg='white', font=('Arial', 11, 'bold'))
email.place(x=350, y=75)

# Password
pass_name = Label(box_2, text='Password:', fg='white', bg='#010F57', font=('Arial', 18, 'bold'))
pass_name.place(x=224, y=119)
passw = Entry(box_2, textvariable=password, width=23, fg='black', border=1, bg='white', font=('Arial', 11, 'bold'),
              show="*")
passw.place(x=350, y=123)
passw.bind("<KeyRelease>", lambda event: update_password_strength())

# Show password
# Password Visibility Toggle Button
show = Image.open("img\\show.jpg")
show_pk = ImageTk.PhotoImage(show.resize((15, 12)))
hide = Image.open("img\\hide.jpg")
hide_pk = ImageTk.PhotoImage(hide.resize((15, 12)))
vis_button = Button(box_2, width=15, height=15, bg='white', bd=0, image=show_pk, command=show_pass)
vis_button.place(x=515, y=126)

# Create the password strength indicator label
strength_label = Label(box_2, text="", font=('Arial', 8, 'bold'), bg='#010F57')
strength_label.place_forget()


# Button
reg = Button(box_2, width=9, pady=6, text="Register", bg='white', cursor='hand2', font=('Arial', 12, 'bold'),
             command=validate_inputs)
reg.place(x=300, y=185)

log = Button(box_2, width=10, pady=6, text="Login", bg='white', cursor='hand2', font=('Arial', 12, 'bold'),
             command=to_sign)
log.place(x=410, y=185)


# Terms and Conditions/DPA Acceptance
checks = BooleanVar()

checks_button = Checkbutton(regist, variable=checks, onvalue=True, offvalue=False, bg='#010F57', bd=0)
checks_button.place(x=328, y=321)

text2 = Label(box_2, text="I agree to E.P.B.I.P", fg='white', bg='#010F57', font=('Arial', 8, 'bold'))
text2.place(x=280, y=242)

trm = Button(box_2, width=17, text='terms and conditions', border=0, bg='#010F57', cursor='hand2', fg='#38B6FF',
             font=('Arial', 8, 'bold', 'underline'), command=show_terms)
trm.place(x=377, y=242)

text3 = Label(box_2, text="and ", fg='white', bg='#010F57', font=('Arial', 8, 'bold'))
text3.place(x=497, y=242)

dpa = Button(box_2, width=14, text='Privacy Policy', border=0, bg='#010F57', cursor='hand2', fg='#38B6FF',
             font=('Arial', 8, 'bold', 'underline'))
dpa.place(x=268, y=258)

regist.mainloop()
