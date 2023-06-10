from __future__ import print_function

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os, base64, email, spampy, json, requests
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
database = firebase.database()
# import firebase_admin
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify']
totalMessages = []
# db = firebase.database()
class EmailScanResult:
    def __init__(self, messageId, urlScore):
        self.messageId = messageId
        self.urlScore = urlScore
def get_messages(service, user_id):
    try:
        EmailScanResult(None, None)
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

messages = []
creds = None

def googleapi():
    """Shows basic usage of the Gmail API.
   Lists the user's Gmail labels.
   """
   
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # if os.path.exists('token.json'):
    #     creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    creds =None
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
        results = service.users().messages().list(userId='me', labelIds=['CATEGORY_PERSONAL'], maxResults=50, q='newer_than:4d').execute()
        # labels = results.get('labels', [])
        # print(results)
        # print(get_messages(service, "me"))
        # email = "Email Subject: " + get_message(service, 'me', '188006a34139969c')["snippet"]
        for i in range(len(results['messages'])):
            message = get_message(service, 'me', results['messages'][i]['id'])
            print(str(i), message)
            messages.append(message)
        dosbg = ttk.Style
        dostable = ttk.Treeview(dos, columns=("Date", "Subject", "Source", "Response"), show="headings")
        # table.pack()

        # Calling pack method w.r.to treeview
        dostable.pack(side='right')

        # root= tk.Tk()
        # dosverscrlbar = ttk.Scrollbar(dostable)
        # dosverscrlbar.pack(side='bottom', fill='y')

        # Constructing vertical scrollbar
        # with treeview
        dosverscrlbar = ttk.Scrollbar(dos,
                                      orient="vertical",
                                      command=dostable.yview)

        # Calling pack method w.r.to vertical
        # scrollbar
        dosverscrlbar.pack(side='right', fill='y')

        # Configuring treeview
        dostable.configure(yscrollcommand=dosverscrlbar.set)

        dostable.heading("Date", text="Date")
        dostable.heading("Subject", text="Subject")
        dostable.heading("Source", text="Analysis")
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
                if samplelist[x]["name"] == "Date":
                    date = samplelist[x]["value"]
            totalMessages.append(message)
            dostable.insert(parent="", index=i, iid=i, text="Row ",
                            values=(date, message["snippet"], "Medium Risk" if emailPredictions[i] == 1 else "No Risk for Spam", "The message has characteristics of a spam message" if emailPredictions[i] == 1 else "No anomaly was found"))
            emctable.insert(parent="", index=i, iid=i, text="Row ",
                            values=(date, message["snippet"], "Medium Risk" if emailPredictions[i] == 1 else "No Risk for Spam", "The message has characteristics of a spam message" if emailPredictions[i] == 1 else "No anomaly was found"))
        dostable.column("Date", width=138)
        dostable.column("Subject", width=400)
        dostable.column("Source", width=200)
        update_chart(dostable)



    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')
def delete(messageId):
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
    service = build('gmail', 'v1', credentials=creds)
    service.users().messages().trash(userId='me', id=messageId).execute()

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
    data.columns
    # data.info()
    # data.isna().sum()
    data['Spam'] = data['Category'].apply(lambda x: 1 if x == 'spam' else 0)

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

def gotoscreens():
        googleapi()
        phishing()

# window
# window
result = Tk()
result.title("E.P.B.I.P")
result.geometry("900x550")
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


def dash():
    result.destroy()
    os.system('Dashboard.py')


# Background
bg_0 = Image.open("img\\bg8.jpg")
bck_pk = ImageTk.PhotoImage(bg_0.resize((900, 550)))

lbl = Label(result, image=bck_pk, border=0)
lbl.place(x=1, y=1)

# Header
box_1 = Frame(result, width=900, height=55, bg='#010F57')
box_1.place(x=3, y=5)
heading = Label(result, text='Detailed Report', fg='white', bg='#010F57', font=('Arial', 30, 'bold'))
heading.place(x=10, y=5)
# widget that manages a collection of windows/displays
notebook = ttk.Notebook(result)
notebook.pack(pady=70)

# Tab results
gback = Button(notebook)
dos = Frame(notebook)
em_c = Frame(notebook)
logo = Frame(notebook)
url = Frame(notebook)
hist = Frame(notebook)
chart = Frame(notebook)

notebook.add(dos, text="Subject\t          ")
notebook.add(em_c, text="All data\t     ")
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
# Label(em_c, text="The email content has been found to be fraudulent.", fg='white', width=75, height=50,
#       bg='#010F57', bd=0, font=('Arial', 9, 'bold')).pack()

# Logo Tab
logo.configure(background='#010F57')
Label(logo, text="The logo has been found to be fraudulent.", fg='white', width=75, height=50,
      bg='#010F57', bd=0, font=('Arial', 9, 'bold')).pack()

# URL Tab
url.configure(background='#010F57')

# History Tab
hist.configure(background='#010F57')
bg = ttk.Style
hist_table = ttk.Treeview(hist, columns=("Date", "Name", "Source", "Response"), show="headings")
# table.pack()

# Calling pack method w.r.to treeview
hist_table.pack(side='right')

# Constructing vertical scrollbar
# with treeview
verscrlbar = ttk.Scrollbar(hist,
                           orient="vertical",
                           command=hist_table.yview)

# Calling pack method w.r.to vertical
# scrollbar
verscrlbar.pack(side='right', fill='y')

# Configuring treeview
hist_table.configure(yscrollcommand=verscrlbar.set)

hist_table.heading("Date", text="Date")
hist_table.heading("Name", text="Name")
hist_table.heading("Source", text="Source")
hist_table.heading("Response", text="Response")
for i in range(1000):
    hist_table.insert(parent="", index=i, iid=i, text="Row 2", values=("03/18/2023 " + str(i), "Click to Win!", "Phishing", "Blocked"))
hist_table.column("Date", minwidth=100)
hist_table.column("Name", width=200)
hist_table.column("Source", width=200)
hist_table.column("Response", width=400)
hist_table.column("Date", minwidth=100)
hist_table.column("Source", width=377)
hist_table.column("Response", width=100)
hist_table.place(y=79)

# Function to update the history table with result data
def update_history_table(data):
    hist_table.delete(*hist_table.get_children())  # Clear existing table entries

    for i, entry in enumerate(data):
        date = entry['date']
        subject = entry['subject']
        response = entry['response']

        hist_table.insert(parent="", index=i, iid=i, text="Row ",
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
        if response == "Medium Risk":
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


emcbg = ttk.Style
emctable = ttk.Treeview(em_c, columns=("Date", "Name", "Source", "Response"), show="headings")
# table.pack()

# Calling pack method w.r.to treeview
emctable.pack(side='right')

# Constructing vertical scrollbar
# with treeview
emctableverscrlbar = ttk.Scrollbar(em_c,
                                   orient="vertical",
                                   command=emctable.yview)

# Calling pack method w.r.to vertical
# scrollbar
emctableverscrlbar.pack(side='right', fill='y')

# Configuring treeview
emctable.configure(yscrollcommand=emctableverscrlbar.set)

emctable.heading("Date", text="Date")
emctable.heading("Name", text="Name")
emctable.heading("Source", text="Analysis")
emctable.heading("Response", text="Response")
emctable.column("Date", minwidth=100)
emctable.column("Name", width=200)
emctable.column("Source", width=200)
emctable.column("Response", width=400)
emctable.place(y=79)

# Chart Tab
chart.configure(background='#010F57')
empty_frame = ttk.Frame(chart, height=100)
fig = Figure(figsize=(4.9, 4), dpi=100)
ax = fig.add_subplot(111)
data = {"Phishing": 2, "Legitimate": 10}
ax.pie(data.values(), labels=data.keys(), shadow=True, explode=(0.1, 0.1), autopct='%1.1f%%', startangle=90)
ax.set_title("Phishing Emails")
canvas = FigureCanvasTkAgg(fig, master=chart)
canvas.draw()
canvas.get_tk_widget().pack(pady=10)

urlbg = ttk.Style
urltable = ttk.Treeview(url, columns=("Email", "Subject", "Source", "Response"), show="headings")
personalMessages = []


def selectItem(a):
    curItem = urltable.focus()
    print(urltable.item(curItem))
def phishing():
    #UI
        # table.pack()

    # Calling pack method w.r.to treeview
    urltable.pack(side='right')

    # Constructing vertical scrollbar
    # with treeview
    urlverscrlbar = ttk.Scrollbar(url,
                                  orient="vertical",
                                  command=urltable.yview)

    # Calling pack method w.r.to vertical
    # scrollbar
    urlverscrlbar.pack(side='right', fill='y')

    # Configuring treeview
    urltable.configure(yscrollcommand=urlverscrlbar.set)

    urltable.heading("Email", text="Email")
    urltable.heading("Subject", text="Subject")
    urltable.heading("Source", text="Analysis")
    urltable.heading("Response", text="Warning")
    #data
    # messageforurl = []
    for i in range(len(messages)):
        # hasPersonalLabel = False
        # for labelIndex in range(len(messages[i]["labelIds"])):
            # if messages[i]["labelIds"][labelIndex] == 'CATEGORY_PERSONAL':
                # hasPersonalLabel = True
        # if hasPersonalLabel == True:
            personalMessages.append(messages[i])

    print("PHISHING MESSAGES:", personalMessages)
    for i in range(len(personalMessages)):
        for headerindex in range(len(personalMessages[i]['payload']["headers"])):
            if personalMessages[i]['payload']["headers"][headerindex]["name"] == 'From':
                messageforurl = ""
                explanationforurl = ""
                fromStringValue = personalMessages[i]['payload']["headers"][headerindex]["value"]
                indexOfAtSign = fromStringValue.find('@')
                domainString = fromStringValue[indexOfAtSign + 1:len(fromStringValue) - 1]
                emailString = fromStringValue
                if domainString == 'gmail.com':
                    messageforurl = ("Low Risk for Phishing")
                    explanationforurl = "The user is using his/her personal email. Legitimate institutions usually use their company email."
                else:
                    indexOfLessThan = fromStringValue.find('<')
                    if indexOfLessThan == -1:
                        emailString = fromStringValue
                        messageforurl = "No Risk for Phishing"
                        explanationforurl = "The user is using a legitimate email associated with their institution."
                    else:
                        emailString = fromStringValue[indexOfLessThan + 1:len(fromStringValue) - 1]
                        # urlString = "https://email-validator8.p.rapidapi.com/api/v2.0/email"
                        urlString = "https://mailcheck.p.rapidapi.com/"

                        querystring = {"domain":emailString}

                        headers = {
                            "X-RapidAPI-Key": "37c32a8b33msh9b757e14e3acd08p18e3c1jsn9b7b63149ada",
                            "X-RapidAPI-Host": "mailcheck.p.rapidapi.com"
                        }

                        # uncomment
                #         response = requests.get(urlString, headers=headers, params=querystring)
                #         if response.json()["disposable"] == True:
                #             messageforurl = "The sender's email is disposable"
                #         else:
                #             messageforurl = "The sender's email looks legitimate."
                # totalMessages.append(personalMessages[i])
                urltable.insert(parent="", index=i, iid=i, text=personalMessages[i]["id"],
                                values=(emailString, personalMessages[i]["snippet"], messageforurl, explanationforurl))
                emctable.insert(parent="", index=i + len(personalMessages), iid=i + len(personalMessages), text=personalMessages[i]["id"],
                                values=(emailString, personalMessages[i]["snippet"], messageforurl, explanationforurl))
    urltable.column("Email", minwidth=100)
    urltable.column("Subject", width=200)
    urltable.column("Source", width=200)
    urltable.column("Response", width=400)
    urltable.place(y=79)
    urltable.bind('<Button-1>', selectItem)


def callback():
    indexSelected = notebook.index(notebook.select())
    if indexSelected == 0:
        print("")
    elif indexSelected == 1:
        if emctable.focus() != '':
            indexToBeDeleted = int(emctable.focus())
            delete(totalMessages[indexToBeDeleted]["id"])
    else:
        print("")

spamButton = Button(result, text="Move to trash", command=callback)
spamButton.place(x=350, y=15)

# Exit Button
result.after(0, gotoscreens)
result.mainloop()
