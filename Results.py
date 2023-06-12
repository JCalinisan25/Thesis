from __future__ import print_function

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import torch
import sys

import os
import base64
from typing import List
import time
from google_apis import create_service
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

import os.path

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

# firebase = pyrebase.initialize_app(config)
# database = firebase.database()
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
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        creds = None
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
        results = service.users().messages().list(userId='me',labelIds=['CATEGORY_PERSONAL'], maxResults=5, q='newer_than:1d').execute()
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
        dosverscrlbar = ttk.Scrollbar(hist,
                                      orient="horizontal",
                                      command=table.xview)

        # Calling pack method w.r.to vertical
        # scrollbar
        dosverscrlbar.pack(side='bottom', fill='x')

        # Configuring treeview
        dostable.configure(xscrollcommand=dosverscrlbar.set)

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
            dostable.insert(parent="", index=len(totalMessages) + 1, iid=len(totalMessages) + 1, text="Row ",
                            values=(date, message["snippet"], "Medium Risk" if emailPredictions[i] == 1 else "No Risk Spam", "The message has characteristics of a spam message" if emailPredictions[i] == 1 else "No anomaly was found"))
            emctable.insert(parent="", index=len(totalMessages) + 1, iid=len(totalMessages) + 1, text="Row ",
                            values=(date, message["snippet"], "Medium Risk" if emailPredictions[i] == 1 else "No Risk Spam", "The message has characteristics of a spam message" if emailPredictions[i] == 1 else "No anomaly was found"))
        dostable.column("Date", minwidth=100)
        dostable.column("Subject", width=200)
        dostable.column("Source", width=200)
        update_chart(dostable)



    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')
def delete(messageId):
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        creds = None
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
    class GmailException(Exception):
        """gmail base exception class"""

    class NoEmailFound(GmailException):
        """no email found"""

    def search_emails(query_string: str, label_ids: List = None):
        try:
            message_list_response = service.users().messages().list(
                userId='me',
                labelIds=label_ids,
                q=query_string
            ).execute()

            message_items = message_list_response.get('messages')
            next_page_token = message_list_response.get('nextPageToken')

            while next_page_token:
                message_list_response = service.users().messages().list(
                    userId='me',
                    labelIds=label_ids,
                    q=query_string,
                    pageToken=next_page_token
                ).execute()

                message_items.extend(message_list_response.get('messages'))
                next_page_token = message_list_response.get('nextPageToken')
            return message_items
        except Exception as e:
            raise NoEmailFound('No emails returned')

    def get_file_data(message_id, attachment_id, file_name, save_location):
        response = service.users().messages().attachments().get(
            userId='me',
            messageId=message_id,
            id=attachment_id
        ).execute()

        file_data = base64.urlsafe_b64decode(response.get('data').encode('UTF-8'))
        return file_data

    def get_message_detail(message_id, msg_format='metadata', metadata_headers: List = None):
        message_detail = service.users().messages().get(
            userId='me',
            id=message_id,
            format=msg_format,
            metadataHeaders=metadata_headers
        ).execute()
        return message_detail

    if __name__ == '__main__':
        CLIENT_FILE = 'credentials.json'
        API_NAME = 'gmail'
        API_VERSION = 'v1'
        SCOPES = ['https://mail.google.com/']
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        else:
            creds = None
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
        query_string = 'has:attachment newer_than:1d'

        save_location = os.getcwd()
        email_messages = search_emails(query_string)

        for email_message in email_messages:
            messageDetail = get_message_detail(email_message['id'], msg_format='full', metadata_headers=['parts'])
            messageDetailPayload = messageDetail.get('payload')

            if 'parts' in messageDetailPayload:
                for msgPayload in messageDetailPayload['parts']:
                    file_name = msgPayload['filename']
                    body = msgPayload['body']
                    if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                        if 'attachmentId' in body:

                            attachment_id = body['attachmentId']
                            attachment_content = get_file_data(email_message['id'], attachment_id, file_name, save_location)

                            with open(os.path.join(save_location, file_name), 'wb') as _f:
                                _f.write(attachment_content)
                                print(f'File \{file_name} is saved at {save_location}')
                                model = torch.hub.load('ultralytics/yolov5','custom', 'best.pt')

                                # img_data = b'base64 string'

                                # with open("path/to/saved_image.jpg", "wb") as fh:
                                #     fh.write(base64.decodebytes(img_data))

                                im = file_name

                                result = model(im)
                                result.print()
                                resultArray = result.pandas().xyxy[0].value_counts('name')
                                messageSnippet = messageDetail["snippet"]
                                message = ""
                                explanation = ""
                                if len(resultArray) == 0:
                                    message = "Possible phishing"
                                    explanation = "Logo is not in the dataset of legit companies"
                                else:
                                    if result.pandas().xyxy[0].value_counts('name').axes[0][0].lower() in messageSnippet.lower():
                                        message = "Not phishing"
                                        explanation = f"Company logo({result.pandas().xyxy[0].value_counts('name').axes[0][0]}) found in the email message"
                                    else:
                                        message = "Possible Phishing"
                                        explanation = "Company logo not found in the email message"

                                totalMessages.append(messageDetail)
                                # urltable.insert(parent="", index=i, iid=i, text=personalMessages[i]["id"],
                                #                 values=(emailString, personalMessages[i]["snippet"], messageforurl,
                                #                         explanationforurl))
                                emctable.insert(parent="", index=len(totalMessages) + 1,
                                                iid=len(totalMessages) + 1, text="",
                                                values=(file_name, messageSnippet, message,
                                                        explanation))
            time.sleep(0.5)
    googleapi()
    phishing()

# window
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
heading.place(x=10, y=5)
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
table = ttk.Treeview(hist, columns=("Date", "Name", "Source", "Response"), show="headings")
# table.pack()

# Calling pack method w.r.to treeview
table.pack(side='right')

# Constructing vertical scrollbar
# with treeview
verscrlbar = ttk.Scrollbar(hist,
                           orient="vertical",
                           command=table.yview)

# Calling pack method w.r.to vertical
# scrollbar
verscrlbar.pack(side='right', fill='y')

# Configuring treeview
table.configure(yscrollcommand=verscrlbar.set)

table.heading("Date", text="Date")
table.heading("Name", text="Name")
table.heading("Source", text="Source")
table.heading("Response", text="Response")
table.insert(parent="", index=1, iid=1, text="Row 2", values=("03/18/2023", "Click to Win!", "Phishing", "Blocked"))
table.column("Date", minwidth=100)
table.column("Name", width=200)
table.column("Source", width=200)
table.column("Response", width=400)
table.place(x=10, y=10)
table.column("Date", minwidth=100)
# table.column("Subject", width=377)
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
    # database.child('Results').push(result_data)

    # Update the history table with the saved data
    # update_history_table(result_data)

# Function to retrieve result data from the database
# def retrieve_result_data():
#     result_data = []
#     results = database.child("Results").get()
#     if results is not None:  # Check if results exist
#         for result in results.each():
#             result_data.append(result.val())
#     return result_data

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


emcbg = ttk.Style
emctable = ttk.Treeview(em_c, columns=("Date", "Name", "Source", "Response"), show="headings")
# table.pack()

# Calling pack method w.r.to treeview
emctable.pack(side='right')

# Constructing vertical scrollbar
# with treeview
emctableverscrlbar = ttk.Scrollbar(hist,
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
emctable.place(x=10, y=10)

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
                                  orient="horizontal",
                                  command=table.xview)

    # Calling pack method w.r.to vertical
    # scrollbar
    urlverscrlbar.pack(side='bottom', fill='x')

    # Configuring treeview
    urltable.configure(xscrollcommand=urlverscrlbar.set)

    urltable.heading("Email", text="Email")
    urltable.heading("Subject", text="Subject")
    urltable.heading("Source", text="Analysis")
    #data
    # messageforurl = []
    for i in range(len(messages)):
        hasPersonalLabel = False
        for labelIndex in range(len(messages[i]["labelIds"])):
            if messages[i]["labelIds"][labelIndex] == 'CATEGORY_PERSONAL':
                hasPersonalLabel = True
        if hasPersonalLabel == True:
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
                    messageforurl = ("Low Risk Phishing")
                    explanationforurl = "The user is using his/her personal email. Legitimate institutions usually use their company email."
                else:
                    indexOfLessThan = fromStringValue.find('<')
                    if indexOfLessThan == -1:
                        emailString = fromStringValue
                        messageforurl = "No Risk Phishing"
                        explanationforurl = "The user is using a legitimate email associated with their institution."
                    else:
                        emailString = fromStringValue[indexOfLessThan + 1:len(fromStringValue) - 1]
                        urlString = "https://email-validator8.p.rapidapi.com/api/v2.0/email"
                        payload = {"email": emailString}
                        headers = {
                            "content-type": "application/x-www-form-urlencoded",
                            "X-RapidAPI-Key": "654c1140e2msh8ec1c8e50fa2531p1e189ejsn4d90f1ce9931",
                            "X-RapidAPI-Host": "email-validator8.p.rapidapi.com"
                        }
                        # uncomment
                        # response = requests.post(urlString, data=payload, headers=headers)
                        # if response.json()["disposable"] == True:
                        #     messageforurl = "The sender's email is disposable"
                        # else:
                        #     messageforurl = "The sender's email looks legitimate."
                totalMessages.append(personalMessages[i])
                urltable.insert(parent="", index=i, iid=i, text=personalMessages[i]["id"],
                                values=(emailString, personalMessages[i]["snippet"], messageforurl, explanationforurl))
                emctable.insert(parent="", index= len(totalMessages) + 1, iid=len(totalMessages) + 1, text=personalMessages[i]["id"],
                                values=(emailString, personalMessages[i]["snippet"], messageforurl, explanationforurl))
    urltable.column("Email", minwidth=100)
    urltable.column("Subject", width=200)
    urltable.column("Source", width=200)
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
Button(notebook, text="X", fg='white', width=1, height=0, bg='#010F57', font=('Arial', 10, 'bold'), bd=0,
       command=dash).place(x=515, y=27)
result.after(0, gotoscreens())
result.mainloop()
