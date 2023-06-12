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



# import firebase_admin
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify']
totalMessages = []

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
    #creds = None
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
        if 'messages' not in results:
            return
        for i in range(len(results['messages'])):
            message = get_message(service, 'me', results['messages'][i]['id'])
            print(str(i), message)
            messages.append(message)
        # table.pack()

        # Constructing vertical scrollbar with treeview
        dostableverscrlbar = ttk.Scrollbar(dos, orient="vertical", command=dostable.yview)

        # Constructing horizontal scrollbar with treeview
        dostablehorscrlbar = ttk.Scrollbar(dos, orient="horizontal", command=dostable.xview)

        # Configuring treeview
        dostable.configure(xscrollcommand=dostablehorscrlbar.set, yscrollcommand=dostableverscrlbar.set)
        dostable.heading("Date", text="Date")
        dostable.heading("Subject", text="Subject")
        dostable.heading("Analysis", text="Analysis")
        dostable.heading("Response", text="Response")
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
                            values=(date, message["snippet"], "Medium Risk" if emailPredictions[i] == 1 else "No Risk for Spam",
                                    "The message has characteristics of a spam message" if emailPredictions[i] == 1 else "No suspicious elements were found."))

            emctable.insert(parent="", index=len(totalMessages), iid=len(totalMessages), text="Row ",
                            values=(date, message["snippet"], "Medium Risk" if emailPredictions[i] == 1 else "No Risk for Spam",
                                    "The message has characteristics of a spam message" if emailPredictions[i] == 1 else "No suspicious elements were found."))
            #hist_table.insert(parent="", index=i, iid=i, text="Row ",
                            #values=(date, message["snippet"], "Medium Risk" if emailPredictions[i] == 1 else "No Risk for Spam",
                                    #"The message has characteristics of a spam message" if emailPredictions[i] == 1 else "No suspicious elements were found."))
        dostable.column("Date", width=180)
        dostable.column("Subject", width=565)
        dostable.column("Analysis", width=130)
        dostable.column("Response", width=330)
        dostable.place(x=0, y=99, width=900, height=250)  # Adjust these values as needed
        dostableverscrlbar.place(x=877, y=0, width=20, height=465)  # Adjust these values as needed
        dostablehorscrlbar.place(x=0, y=445, width=877, height=20)  # Adjust these values as needed
        update_chart_spam(dostable)

        #save_to_history(dostable)
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
        # creds = None
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

        logotable.pack(side='left')
        logoverscrlbar = ttk.Scrollbar(dos,
                                      orient="vertical",
                                      command=logotable.yview)
        logoverscrlbar.pack(side='left', fill='y')
        logotable.configure(yscrollcommand=logoverscrlbar.set)
        logotable.heading("Logo", text="Logo")
        logotable.heading("Subject", text="Subject")
        logotable.heading("Analysis", text="Analysis")
        if email_messages is not None:
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
                                    print(f'File {file_name} is saved at {save_location}')
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
                                    emctable.insert(parent="", index=len(totalMessages),
                                                    iid=len(totalMessages), text="",
                                                    values=(file_name, messageSnippet, message,
                                                            explanation))
                                    logotable.insert(parent="", index=len(totalMessages),
                                                    iid=len(totalMessages), text="",
                                                    values=(file_name, messageSnippet, message,
                                                            explanation))
                time.sleep(0.5)
    googleapi()
    phishing()

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

def update_heading(event):
    selected_tab = notebook.tab(notebook.select(), "text")
    heading.config(text=selected_tab)


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


def update_tab_title(event):
    selected_tab = notebook.tab(notebook.select(), "text")
    result.title(f"Detailed Report - {selected_tab}")

# widget that manages a collection of windows/displays
notebook = ttk.Notebook(result, height=465, width = 895)
notebook.place(x=1,y=60)

# Bind the event to update the tab title
notebook.bind("<<NotebookTabChanged>>", update_tab_title)

# Tab results
gback = Button(notebook)
dos = Frame(notebook)
em_c = Frame(notebook)
logo = Frame(notebook)
url = Frame(notebook)
hist = Frame(notebook)
chart = Frame(notebook)

notebook.add(em_c, text="Summary\t     ")
notebook.add(dos, text="Subject\t          ")
notebook.add(url, text="URL/s\t    ")
notebook.add(logo, text="Logo\t    ")
notebook.add(hist, text="History\t    ")
notebook.add(chart, text="Chart\t    ")

# Set the initial window title
result.title("Detailed Report - Summary")

# Bind the tab change event to the update_heading function
notebook.bind("<<NotebookTabChanged>>", update_heading)

# Domain Tab
dos.configure(background='#010F57')
dosbg = ttk.Style
dostable = ttk.Treeview(dos, columns=("Date", "Subject", "Analysis"), show="headings")
logotable = ttk.Treeview(logo, columns=("Logo", "Subject", "Analysis"), show="headings")
# Label(dos, text="The domain '@d1scord.com' has been found to be fraudulent. "
#                 "\nIt appears to be mimicking 'discord.com'.", fg='white', width=75, height=50,
#       bg='#010F57', bd=0, font=('Arial', 9, 'bold')).pack()

# Email Tab
em_c.configure(background='#010F57')
# Label(em_c, text="The email content has been found to be fraudulent.", fg='white', width=75, height=50,
#       bg='#010F57', bd=0, font=('Arial', 9, 'bold')).pack()

# Logo Tab
logo.configure(background='#010F57')
# Label(logo, text="The  has been found to be fraudulent.", fg='white', width=75, height=50,
#       bg='#010F57', bd=0, logofont=('Arial', 9, 'bold')).pack()

# URL Tab
url.configure(background='#010F57')


# Function to save email data to the database
# Function to update the history table with result data
def update_history_table(data):
    hist_table.delete(*hist_table.get_children())  # Clear existing table entries
    
    for i, entry in enumerate(data):
        date = entry['date']
        subject = entry['subject']
        analysis = entry['analysis']


        hist_table.insert(parent="", index=i, iid=i, text="Row ",
                          values=(date, subject, analysis))

# Function to retrieve result data from dostable and urltable and save it to the history tab
def save_to_history( urltable):
    dos_items = dostable.get_children()  # Get all items in dostable
    url_items = urltable.get_children()  # Get all items in urltable
    
    result_data = []

    for item in dos_items:
        values = dostable.item(item)['values']
        date = values[0]
        subject = values[1]
        analysis = values[2]

        
        result_data.append({
            'date': date,
            'subject': subject,
            'analysis': analysis,

        })

    for item in url_items:
        values = urltable.item(item)['values']
        date = values[0]
        subject = values[1]
        analysis = values[2]


        result_data.append({
            'date': date,
            'subject': subject,
            'analysis': analysis,

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


# History Tab
hist.configure(background='#010F57')
bg = ttk.Style
hist_table = ttk.Treeview(hist, columns=("Date", "Subject", "Analysis", "Response"), show="headings")
# table.pack()

# Constructing vertical scrollbar with treeview
histtableverscrlbar = ttk.Scrollbar(hist, orient="vertical", command=hist_table.yview)

# Constructing horizontal scrollbar with treeview
histtablehorscrlbar = ttk.Scrollbar(hist, orient="horizontal", command=hist_table.xview)

# Configuring treeview
hist_table.configure(xscrollcommand=histtablehorscrlbar.set, yscrollcommand=histtableverscrlbar.set)
hist_table.heading("Date", text="Details")
hist_table.heading("Subject", text="Subject")
hist_table.heading("Analysis", text="Analysis")
hist_table.heading("Response", text="Response")
hist_table.column("Date", minwidth=240)
hist_table.column("Subject", width=510)
hist_table.column("Analysis", width=130)
hist_table.column("Response", width=400)

# Place treeview and scrollbars
hist_table.place(x=0, y=99, width=900, height=250)  # Adjust these values as needed
histtableverscrlbar.place(x=877, y=0, width=20, height=465)  # Adjust these values as needed
histtablehorscrlbar.place(x=0, y=445, width=877, height=20)  # Adjust these values as needed


# Function to update the chart with percentages of flagged and not flagged emails
def update_chart_spam(dostable):
    items = dostable.get_children()  # Get all items in dostable
    total_emails = len(items)
    flagged_emails = 0

    for item in items:
        response = dostable.item(item)['values'][2]
        if response == "Medium Risk":
            flagged_emails += 1

    not_flagged_emails = total_emails - flagged_emails
    percentages = {
        "Spam": flagged_emails / total_emails * 100,
        "Normal": not_flagged_emails / total_emails * 100
    }

    statistics = f"Total Emails: {total_emails}\nFlagged Emails: {flagged_emails}\nNormal Emails: {not_flagged_emails}"

    ax2.clear()  # Clear the existing chart
    ax2.pie(percentages.values(), labels=percentages.keys(), shadow=True, explode=(0.1, 0.1), autopct='%1.1f%%', startangle=90)
    ax2.set_title("Spam Emails")
    ax2.text(0.1, 0.01, statistics, horizontalalignment='center', verticalalignment='center', transform=ax1.transAxes)
    canvas.draw()



#Function to update the chart with percentages of flagged and not flagged emails
def update_chart_phish(urltable):
    items = urltable.get_children()  # Get all items in dostable
    total_emails = len(items)
    flagged_emails = 0

    for item in items:
        analysis = urltable.item(item)['values'][2]
        if analysis == "Low Risk for Phishing" or analysis == "The sender's email is disposable":
            flagged_emails += 1

    not_flagged_emails = total_emails - flagged_emails
    percentages = {
        "Phishing": flagged_emails / total_emails * 100,
        "Normal": not_flagged_emails / total_emails * 100
    }

    statistics = f"Total Emails: {total_emails}\nFlagged Emails: {flagged_emails}\nNormal Emails: {not_flagged_emails}"

    ax1.clear()  # Clear the existing chart
    ax1.pie(percentages.values(), labels=percentages.keys(), shadow=True, explode=(0.1, 0.1), autopct='%1.1f%%', startangle=90)
    ax1.set_title("Phishing Emails")
    ax1.text(0.1, 0.01, statistics, horizontalalignment='center', verticalalignment='center', transform=ax1.transAxes)
    canvas.draw()


emcbg = ttk.Style
emctable = ttk.Treeview(em_c, columns=("Date", "Subject", "Analysis", "Response"), show="headings")
# table.pack()

# Constructing vertical scrollbar with treeview
emctableverscrlbar = ttk.Scrollbar(em_c, orient="vertical", command=emctable.yview)

# Constructing horizontal scrollbar with treeview
emctablehorscrlbar = ttk.Scrollbar(em_c, orient="horizontal", command=emctable.xview)

# Configuring treeview
emctable.configure(xscrollcommand=emctablehorscrlbar.set, yscrollcommand=emctableverscrlbar.set)

emctable.heading("Date", text="Details")
emctable.heading("Subject", text="Subject")
emctable.heading("Analysis", text="Analysis")
emctable.heading("Response", text="Response")
emctable.column("Date", minwidth=240)
emctable.column("Subject", width=510)
emctable.column("Analysis", width=130)
emctable.column("Response", width=450)

# Place treeview and scrollbars
emctable.place(x=0, y=99, width=900, height=250)  # Adjust these values as needed
emctableverscrlbar.place(x=877, y=0, width=20, height=465)  # Adjust these values as needed
emctablehorscrlbar.place(x=0, y=445, width=877, height=20)  # Adjust these values as needed


# Chart Tab
chart.configure(background='#010F57')
empty_frame = ttk.Frame(chart, height=100)
fig1 = Figure(figsize=(4.2, 4), dpi=100)
ax1 = fig1.add_subplot(111)
canvas = FigureCanvasTkAgg(fig1, master=chart)
canvas.get_tk_widget().pack(side=LEFT,pady=10, padx=20)

fig2 = Figure(figsize=(3.9, 4), dpi=100)
ax2 = fig2.add_subplot(111)
canvas = FigureCanvasTkAgg(fig2, master=chart)
canvas.get_tk_widget().pack(side=RIGHT,pady=10, padx=20)

urlbg = ttk.Style
urltable = ttk.Treeview(url, columns=("Email", "Subject", "Source", "Response"), show="headings")
personalMessages = []


def selectItem(a):
    curItem = urltable.focus()
    print(urltable.item(curItem))

def phishing():
    #UI

        # table.pack()
    # Constructing vertical scrollbar with treeview
    urltableverscrlbar = ttk.Scrollbar(url, orient="vertical", command=urltable.yview)

    # Constructing horizontal scrollbar with treeview
    urltablehorscrlbar = ttk.Scrollbar(url, orient="horizontal", command=urltable.xview)

    # Configuring treeview
    urltable.configure(xscrollcommand=urltablehorscrlbar.set, yscrollcommand=urltableverscrlbar.set)
    urltable.heading("Email", text="Email")
    urltable.heading("Subject", text="Subject")
    urltable.heading("Source", text="Analysis")
    urltable.heading("Response", text="Response")
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
                if domainString == 'gmail.com' or domainString == "yahoo.com":
                    messageforurl = "Medium Risk for Phishing"
                    explanationforurl = "The email of the sender is a personal email."
                else:
                    indexOfLessThan = fromStringValue.find('<')
                    if indexOfLessThan == -1:
                        emailString = fromStringValue
                        messageforurl = "Low Risk for Phishing"
                        explanationforurl = "The sender's email is a legitimate email associated with their institution."
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
                totalMessages.append(personalMessages[i])
                urltable.insert(parent="", index=i, iid=i, text=personalMessages[i]["id"],
                                values=(emailString, personalMessages[i]["snippet"], messageforurl))
                emctable.insert(parent="", index=len(totalMessages), iid=len(totalMessages), text=personalMessages[i]["id"],
                                values=(emailString, personalMessages[i]["snippet"], messageforurl, explanationforurl))
                #hist_table.insert(parent="", index=i + len(personalMessages), iid=i + len(personalMessages), text=personalMessages[i]["id"],
                                #values=(emailString, personalMessages[i]["snippet"], messageforurl, explanationforurl))
    
                urltable.column("Email", minwidth=240)
                urltable.column("Subject", width=515)
                urltable.column("Source", width=120)
                urltable.column("Response", width=450)
                urltable.bind('<Button-1>', selectItem)
                update_chart_phish(urltable)
                save_to_history(urltable)


    # Place treeview and scrollbars
    urltable.place(x=0, y=99, width=900, height=250)  # Adjust these values as needed
    urltableverscrlbar.place(x=877, y=0, width=20, height=465)  # Adjust these values as needed
    urltablehorscrlbar.place(x=0, y=445, width=877, height=20)  # Adjust these values as needed

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


def todash():
    result.destroy()
    os.system("Dashboard.py")

spamButton = Button(result, text="Move to trash", command=callback)
spamButton.place(x=350, y=15)

bck_btn = Button(result, text="Return to dashboard", command=todash)
bck_btn.place(x=770, y=15)

# Exit Button
result.after(0, gotoscreens)
result.mainloop()
