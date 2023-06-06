from __future__ import print_function

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os, base64, email, spampy, json
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
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os.path, pyrebase

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
result = Tk()
result.title("E.P.B.I.P")
result.geometry("700x550")
result.resizable(False, False)
result.iconbitmap(r'img\\logo.ico')

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
center_window(result)

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
    """if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)"""
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
        results = service.users().messages().list(userId='me', q='newer_than:1d').execute()
        # labels = results.get('labels', [])
        print(results)
        # print(get_messages(service, "me"))
        # email = "Email Subject: " + get_message(service, 'me', '188006a34139969c')["snippet"]
        messages = []
        for i in range(len(results['messages'])):
            messages.append(get_message(service, 'me', results['messages'][i]['id']))
        dosbg = ttk.Style
        dostable = ttk.Treeview(dos, columns=("Date", "Subject", "Source", "Response"), show="headings")
        # table.pack()

        # Calling pack method w.r.to treeview
        dostable.pack(side='right')

        # Constructing vertical scrollbar
        # with treeview
        dosverscrlbar = ttk.Scrollbar(hist, orient="vertical", command=table.yview)

        # Calling pack method w.r.to vertical
        # scrollbar
        dosverscrlbar.pack(side='right', fill='y')

        # Configuring treeview
        dostable.configure(yscrollcommand=dosverscrlbar.set)

        dostable.heading("Date", text="Date")
        dostable.heading("Subject", text="Subject")
        dostable.heading("Source", text="Result")
        subjectsToPredict = []
        for i in range(len(messages)):
            subjectsToPredict.append(messages[i]["snippet"])
        print(subjectsToPredict)
        emailPredictions = main2(subjectsToPredict)
        print(emailPredictions)
        print(messages)
        for i in range(len(messages)):
            message = messages[i]

            samplelist = message["payload"]["headers"]
            date = ''

            for x in range(len(samplelist)):
                print(samplelist[x])
                if samplelist[x]["name"] == "Date":
                    date = samplelist[x]["value"]


            dostable.insert(parent="", index=i, iid=i, text="Row ",
                            values=(date, message["snippet"], "Flagged" if emailPredictions[i] == 1 else "Not Flagged"))
        # dostable.insert(parent="", index=1, iid=1, text="Row 2",
        # values=("03/18/2023", "Click to Win!", "Phishing", "Blocked"))
        dostable.column("Date", minwidth=100)
        dostable.column("Subject", width=400)
        dostable.column("Source", width=100)

        # print(email)
        # if not labels:
        #     print('No labels found.')
        #     return
        # print('Labels:')
        # for label in labels:
        #     print(label['name'])
        
        # Update the chart with percentages
        update_chart(dostable)


    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')

    # Call the save_to_history function and pass the dostable object
    save_to_history(dostable)  # Save and update history table


def main2(emails):
    for dirname, _, filenames in os.walk('/kaggle/input'):
        for filename in filenames:
            print(os.path.join(dirname, filename))

    # You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All"
    # You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session
    return printhi(emails)


def printhi(emails):
    # Use a breakpoint in the code line below to debug your script.
    data = pd.read_csv('spam.csv')
    # print(data)
    data.columns
    # data.info()
    # data.isna().sum()
    data['Spam'] = data['Category'].apply(lambda x: 1 if x == 'spam' else 0)
    # print(data.head(5))

    X_train, X_test, y_train, y_test = train_test_split(data.Message, data.Spam, test_size=0.5)

    # for dirname, _, filenames in os.walk('/kaggle/input'):
    #     for filename in filenames:
    #         print(os.path.join(dirname, filename))

    clf = Pipeline([
        ('vectorizer', CountVectorizer()),
        ('nb', MultinomialNB())
    ])
    clf.fit(X_train, y_train)
    print(clf.predict(emails))
    return clf.predict(emails)
    # print("prediction: ", clf.score(X_test, y_test))
    # print(clf.predict(emails))


def dash():
    result.destroy()
    os.system('Dashboard.py')


# Background
bg_0 = Image.open("img\\bg8.jpg")
bck_pk = ImageTk.PhotoImage(bg_0.resize((700, 550)))

lbl = Label(result, image=bck_pk, border=0)
lbl.place(x=1, y=1)

# Header
box_1 = Frame(result, width=700, height=55, bg='#010F57')
box_1.place(x=3, y=5)
heading = Label(result, text='Detailed Report', fg='white', bg='#010F57', font=('Arial', 30, 'bold'))
heading.place(x=130, y=5)

# widget that manages a collection of windows/displays
notebook = ttk.Notebook(result)
notebook.pack(pady=70)

error = Image.open("img\\error.PNG")
ror_pk = ImageTk.PhotoImage(error.resize((100, 100)))

lbl = Label(notebook, image=ror_pk, border=0)
lbl.place(x=230, y=190)

# Tab results
gback = Button(notebook)
dos = Frame(notebook)
em_c = Frame(notebook)
logo = Frame(notebook)
url = Frame(notebook)
hist = Frame(notebook)
chart = Frame(notebook)

notebook.add(dos, text="Domain of Sender\t          ")
notebook.add(em_c, text="Email Content\t     ")
notebook.add(logo, text="Logo\t    ")
notebook.add(url, text="URL/s\t    ")
notebook.add(hist, text="History\t    ")
notebook.add(chart, text="Chart\t    ")

# Domain Tab
dos.configure(background='#010F57')
# Label(dos, text="The domain '@d1scord.com' has been found to be fraudulent. "
#                 "\nIt appears to be mimicking 'discord.com'.", fg='white', width=75, height=50,
#       bg='#010F57', bd=0, font=('Arial', 9, 'bold')).pack()

# Email Tab
em_c.configure(background='#010F57')
Label(em_c, text="The email content has been found to be fraudulent.", fg='white', width=75, height=50,
      bg='#010F57', bd=0, font=('Arial', 9, 'bold')).pack()

# Logo Tab
logo.configure(background='#010F57')
Label(logo, text="The logo has been found to be fraudulent.", fg='white', width=75, height=50,
      bg='#010F57', bd=0, font=('Arial', 9, 'bold')).pack()

# URL Tab
url.configure(background='#010F57')
Label(url, text="The URL has been found a phishing site.", fg='white', width=75, height=50,
      bg='#010F57', bd=0, font=('Arial', 9, 'bold')).pack()

# History Tab
hist.configure(background='#010F57')
bg = ttk.Style
table = ttk.Treeview(hist, columns=("Date", "Subject", "Response"), show="headings")
table.grid(row=0, column=1, sticky="nsew")
# table.pack()

# Calling pack method w.r.to treeview


# Constructing vertical scrollbar
# with treeview
verscrlbar = ttk.Scrollbar(hist, orient="vertical", command=table.yview)

# Calling pack method w.r.to vertical
# scrollbar


# Configuring treeview
table.configure(yscrollcommand=verscrlbar.set)

table.heading("Date", text="Date")
table.heading("Subject", text="Subject")
table.heading("Response", text="Response")
table.column("Date", minwidth=100)
table.column("Subject", width=377)
table.column("Response", width=100)
table.place(y=79)

# Function to update the history table with result data
def update_history_table(data):
    table.delete(*table.get_children())  # Clear existing table entries
    
    for i, entry in enumerate(data):
        date = entry['date']
        subject = entry['subject']
        response = entry['response']
        
        table.insert(parent="", index=i, iid=i, text="Row ",
                     values=(date, subject, response))

# Function to retrieve result data from dostable and save it to the history tab
def save_to_history(dostable):
    items = dostable.get_children()  # Get all items in dostable
    
    result_data = []
    for item in items:
        values = dostable.item(item)['values']
        date = values[0]
        subject = values[1]
        response = values[2]
        
        result_data.append({
            'date': date,
            'subject': subject,
            'response': response
        })
    
    # Save the result data to the database
    database.child('Results').push(result_data)
    
    # Update the history table with the saved data
    update_history_table(result_data)

# Function to retrieve result data from the database
def retrieve_result_data():
    result_data = []
    results = database.child("Results").get()
    if results is not None:  # Check if results exist
        for result in results.each():
            result_data.append(result.val())
    return result_data

# Function to update the chart with percentages of flagged and not flagged emails
def update_chart(dostable):
    items = dostable.get_children()  # Get all items in dostable
    total_emails = len(items)
    flagged_emails = 0
    
    for item in items:
        response = dostable.item(item)['values'][2]
        if response == "Flagged":
            flagged_emails += 1
    
    not_flagged_emails = total_emails - flagged_emails
    percentages = {
        "Phishing": flagged_emails / total_emails * 100,
        "Normal": not_flagged_emails / total_emails * 100
    }
    
    statistics = f"Total Emails: {total_emails}\nFlagged Emails: {flagged_emails}\nNot Flagged Emails: {not_flagged_emails}"
    
    ax.clear()  # Clear the existing chart
    ax.pie(percentages.values(), labels=percentages.keys(), shadow=True, explode=(0.1, 0.1), autopct='%1.1f%%', startangle=90)
    ax.set_title("Phishing Emails")
    ax.text(0.5, -0.25, statistics, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
    canvas.draw()


# Chart Tab
chart.configure(background='#010F57')
empty_frame = ttk.Frame(chart, height=100)
fig = Figure(figsize=(3, 5.5), dpi=100)  # Increase the size of the chart
ax = fig.add_subplot(111)
data = {"Phishing": 2, "Legitimate": 10}
ax.pie(data.values(), labels=data.keys(), shadow=True, explode=(0.1, 0.1), autopct='%1.1f%%', startangle=90)
ax.set_title("Phishing Emails")
canvas = FigureCanvasTkAgg(fig, master=chart)
canvas.draw()
canvas.get_tk_widget().pack(pady=10)

# Exit Button
Button(notebook, text="X", fg='white', width=1, height=0, bg='#010F57', font=('Arial', 10, 'bold'), bd=0,
       command=dash).place(x=680, y=27)
result.after(0, main)
result.mainloop()
