from __future__ import print_function

from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os, re, pyrebase, json
import base64
import email
import spampy
from google_auth_oauthlib.flow import InstalledAppFlow
from urlchecker.core.urlproc import UrlCheckResult


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)


# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


import os.path


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_messages(service, user_id):
   try:
       return service.users().messages().list(userId=user_id).execute()
   except Exception as error:
       print('An error occurred: %s' % error)


def get_message(service, user_id, msg_id):
   try:
       return service.users().messages().get(userId=user_id, id=msg_id, format='metadata').execute()
   except Exception as error:
       print('An error occurred: %s' % error)


def get_mime_message(service, user_id, msg_id):
   try:
       message = service.users().messages().get(userId=user_id, id=msg_id,
                                                format='raw').execute()
       print('Message snippet: %s' % message['snippet'])
       msg_str = base64.urlsafe_b64decode(message['raw'].encode("utf-8")).decode("utf-8")
       mime_msg = email.message_from_string(msg_str)
       return mime_msg
   except Exception as error:
       print('An error occurred: %s' % error)


def main():
   """Shows basic usage of the Gmail API.
   Lists the user's Gmail labels.
   """
   creds = None
   # The file token.json stores the user's access and refresh tokens, and is
   # created automatically when the authorization flow completes for the first
   # time.
   if os.path.exists('token.json'):
       creds = Credentials.from_authorized_user_file('token.json', SCOPES)
   # If there are no (valid) credentials available, let the user log in.
   if not creds or not creds.valid:
       if creds and creds.expired and creds.refresh_token:
           creds.refresh(Request())
       else:
           flow = InstalledAppFlow.from_client_secrets_file(
               'credentials.json', SCOPES)
           creds = flow.run_local_server(port=0)
       # Save the credentials for the next run
       with open('token.json', 'w') as token:
           token.write(creds.to_json())


   try:
       # Call the Gmail API
       service = build('gmail', 'v1', credentials=creds)
       results = service.users().labels().list(userId='me').execute()
       labels = results.get('labels', [])


       print(get_messages(service, "me"))
       email = "Email Subject: " + get_message(service, 'me', '188006a34139969c')["snippet"]


       print(email)
       # if not labels:
       #     print('No labels found.')
       #     return
       # print('Labels:')
       # for label in labels:
       #     print(label['name'])


   except HttpError as error:
       # TODO(developer) - Handle errors from gmail API.
       print(f'An error occurred: {error}')


def main2():




   for dirname, _, filenames in os.walk('/kaggle/input'):
       for filename in filenames:
           print(os.path.join(dirname, filename))


   # You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All"
   # You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


   def print_hi(name):
       # Use a breakpoint in the code line below to debug your script.
       data = pd.read_csv('spam.csv')
       # print(data)
       data.columns
       # data.info()
       # data.isna().sum()
       data['Spam'] = data['Category'].apply(lambda x: 1 if x == 'spam' else 0)
       print(data.head(5))


       X_train, X_test, y_train, y_test = train_test_split(data.Message, data.Spam, test_size=0.25)


       # for dirname, _, filenames in os.walk('/kaggle/input'):
       #     for filename in filenames:
       #         print(os.path.join(dirname, filename))


       clf = Pipeline([
           ('vectorizer', CountVectorizer()),
           ('nb', MultinomialNB())
       ])
       clf.fit(X_train, y_train)
       emails = ["Hi goodmorning how are you!",
                 "Hi if ur lookin 4 saucy daytime fun wiv busty married woman Am free all next week Chat now 2 sort time 09099726429 JANINExx Calls£1/minMobsmoreLKPOBOX177HP51FL "
                 ]
       clf.predict(emails)
       print("prediction: ", clf.score(X_test, y_test))
       print(clf.predict(emails))

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
usernm = Entry(box_2, width=25, fg='#9098ba', border=0, bg='white', font=('Arial', 11, 'bold'), show="")
usernm.place(x=50, y=125)
usernm.insert(0, 'Example@email.com')
usernm.bind('<FocusIn>', on_entry)
usernm.bind('<FocusOut>', on_password)
usernm.bind('<Button-1>', remove_focus)
Frame(box_2, width=205, height=2, bg='#010F57').place(x=48, y=145)

# Password
passw = Entry(box_2, width=22, fg='#9098ba', border=0, bg='white', font=('Arial', 11, 'bold'), show="")
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
Button(box_2, width=20, pady=5, text="Sign In", bg='#021976', fg='white', cursor='hand2', font=('Arial', 12, 'bold'),
       command=invalid, bd=0).place(x=48, y=245)

# Forgot password
f_pass = Button(box_2, width=15, text='Forgot Password?', border=0, bg='white', cursor='hand2', fg='#021976',
                font=('Arial', 9), command=forgot)
f_pass.place(x=45, y=205)

# To Register
to_reg = Label(box_2, text="Don't have an account?", fg='#021976', bg='white', font=('Arial', 9))
to_reg.place(x=60, y=295)

sign_up = Button(box_2, width=6, text='Sign up', border=0, bg='white', cursor='hand2', fg='#021976',
                 font=('Arial', 9, 'bold', 'underline'), command=toreg)
sign_up.place(x=195, y=295)

login.mainloop()
