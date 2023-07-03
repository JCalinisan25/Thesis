from __future__ import print_function

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import torch
import seaborn as sns
from csv import writer


import os
import base64
from typing import List
import time
from google_apis import create_service
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
summarydictionary = dict()


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
        results = service.users().messages().list(userId='me', maxResults=5, q='newer_than:1d').execute()
        #,labelIds=['CATEGORY_PERSONAL']
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
        dostable.heading("Date", text="Date", anchor="center")
        dostable.heading("Subject", text="Subject", anchor="center")
        dostable.heading("Analysis", text="Analysis", anchor="center")
        dostable.heading("Response", text="Response", anchor="center")
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
            # totalMessages.append(message)
            dostable.insert(parent="", index=i, iid=i, text="Row ",
                            values=(date, message["snippet"], "Medium Risk for Spam" if emailPredictions[i] == 1 else "No Risk for Spam",
                                    "The message has characteristics of a spam message" if emailPredictions[i] == 1 else "No suspicious elements were found."))
            # emctable.insert(parent="", index=len(totalMessages), iid=len(totalMessages), text="Row ",
            #                 values=(date, message["snippet"], "Medium Risk for Spam" if emailPredictions[i] == 1 else "No Risk for Spam",
            #                         "The message has characteristics of a spam message" if emailPredictions[i] == 1 else "No suspicious elements were found."))
            if message["id"] not in summarydictionary:
                summarydictionary[message["id"]] = dict()
                summarydictionary[message["id"]]["score"] = 0
                summarydictionary[message["id"]]["totalscore"] = 0
            summarydictionary[message["id"]]["score"] = summarydictionary[message["id"]]["score"] + ( 0 if emailPredictions[i] == 1 else 25)
            summarydictionary[message["id"]]["totalscore"] = summarydictionary[message["id"]]["totalscore"] + 25
            summarydictionary[message["id"]]["details"] = message

            #hist_table.insert(parent="", index=i, iid=i, text="Row ",
                            #values=(date, message["snippet"], "Medium Risk" if emailPredictions[i] == 1 else "No Risk for Spam",
                                    #"The message has characteristics of a spam message" if emailPredictions[i] == 1 else "No suspicious elements were found."))

        dostable.column("Date", width=180, anchor="w")
        dostable.column("Subject", width=565, anchor="w")
        dostable.column("Analysis", width=130, anchor="w")
        dostable.column("Response", width=330, anchor="w")
        dostable.place(x=0, y=1, width=1513, height=752)  # Adjust these values as needed
        dostableverscrlbar.place(x=1513, y=0, width=20, height=755)  # Adjust these values as needed
        #dostablehorscrlbar.place(x=0, y=445, width=877, height=20)  # Adjust these values as needed

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


def delete(messageDetails):
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
    service.users().messages().trash(userId='me', id=messageDetails["id"]).execute()
    if checkboxvariable.get() == 1:
        data = {
            'Category': ['spam'],
            'Message': [messageDetails["snippet"]]
        }

        # Make data frame of above data
        df = pd.DataFrame(data)

        # append data frame to CSV file
        df.to_csv('spam.csv', mode='a', index=False, header=False)
        # with open('spam.csv', 'a') as f_object:
        #     # Pass this file object to csv.writer()
        #     # and get a writer object
        #     writer_object = writer(f_object)
        #
        #     # Pass the list as an argument into
        #     # the writerow()
        #     writer_object.writerow(["ham", messageDetails["snippet"]])
        #
        #     # Close the file object
        #     f_object.close()

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

        # Constructing vertical scrollbar with treeview
        logtableverscrlbar = ttk.Scrollbar(logo, orient="vertical", command=logotable.yview)

        # Constructing horizontal scrollbar with treeview
        logtablehorscrlbar = ttk.Scrollbar(logo, orient="horizontal", command=logotable.xview)

        # Configuring treeview
        logotable.configure(xscrollcommand=logtablehorscrlbar.set, yscrollcommand=logtableverscrlbar.set)
        logotable.heading("Logo", text="Logo", anchor="center")
        logotable.heading("Subject", text="Subject", anchor="center")
        logotable.heading("Analysis", text="Analysis", anchor="center")
        logotable.heading("Response", text="Response", anchor="center")
        logotable.column("Logo", width=180, anchor="w")
        logotable.column("Subject", width=565, anchor="w")
        logotable.column("Analysis", width=130, anchor="w")
        logotable.column("Response", width=300, anchor="w")
        logotable.place(x=0, y=1, width=1513, height=752)  # Adjust these values as needed
        logtableverscrlbar.place(x=1513, y=0, width=20, height=755)  # Adjust these values as needed
        #logtablehorscrlbar.place(x=0, y=445, width=877, height=20)  # Adjust these values as needed
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
                                    logoscore = 0
                                    message = ""
                                    explanation = ""
                                    if len(resultArray) == 0:
                                        message = "Possible phishing"
                                        explanation = "Logo is not in the dataset of legit companies"
                                    else:
                                        if result.pandas().xyxy[0].value_counts('name').axes[0][0].lower() in messageSnippet.lower():
                                            message = "Not phishing"
                                            logoscore = 25
                                            explanation = f"Company logo({result.pandas().xyxy[0].value_counts('name').axes[0][0]}) found in the email message"
                                        else:
                                            message = "Possible Phishing"
                                            explanation = "Company logo not found in the email message"
                                            logoscore = 12

                                    # totalMessages.append(messageDetail)
                                    # urltable.insert(parent="", index=i, iid=i, text=personalMessages[i]["id"],
                                    #                 values=(emailString, personalMessages[i]["snippet"], messageforurl,
                                    #                         explanationforurl))
                                    # emctable.insert(parent="", index=len(totalMessages),
                                    #                 iid=len(totalMessages), text="",
                                    #                 values=(file_name, messageSnippet, message,
                                    #                         explanation))
                                    logotable.insert(parent="", index=len(totalMessages),
                                                    iid=len(totalMessages), text="",
                                                    values=(file_name, messageSnippet, message,
                                                            explanation))
                                    # if email_message["id"] not in summarydictionary:
                                    summarydictionary[email_message["id"]] = dict()
                                    summarydictionary[email_message["id"]]["totalscore"] = 25
                                    summarydictionary[email_message["id"]]["score"] = logoscore
                time.sleep(0.5)
    googleapi()
    phishing()

# window
result = Tk()
result.title("E.P.B.I.P")
result.resizable(False, False)
result.state('zoomed')
result.iconbitmap(r'img\\logo.ico')


def dash():
    result.destroy()
    os.system('Dashboard.py')

def update_heading(event):
    selected_tab = notebook.tab(notebook.select(), "text")
    heading.config(text=selected_tab)


# Background
bg_0 = Image.open("img\\bg8.jpg")
bck_pk = ImageTk.PhotoImage(bg_0.resize((1535, 840)))

lbl = Label(result, image=bck_pk, border=0)
lbl.place(x=1, y=1)

# Header
box_1 = Frame(result, width=1535, height=55, bg='#010F57')
box_1.place(x=3, y=5)
heading = Label(result, text='Detailed Report', fg='white', bg='#010F57', font=('Arial', 30, 'bold'))
heading.place(x=10, y=5)


def update_tab_title(event):
    selected_tab = notebook.tab(notebook.select(), "text")
    result.title(f"Detailed Report - {selected_tab}")

# Create a custom style for the notebook
style = ttk.Style()
style.configure("Bold.TNotebook.Tab", font=('Arial', 12, 'bold'))

# widget that manages a collection of windows/displays
notebook = ttk.Notebook(result, height=755, width = 1533, style="Bold.TNotebook")
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

notebook.add(em_c, text="Summary\t\t\t     ")
notebook.add(dos, text="Subject\t\t\t      ")
notebook.add(url, text="URL/s\t\t\t    ")
notebook.add(logo, text="Logo\t\t\t    ")
notebook.add(hist, text="History\t\t\t    ")
notebook.add(chart, text="Chart\t\t\t ")

# Bind the tab change event to the update_heading function
notebook.bind("<<NotebookTabChanged>>", update_heading)

# Domain Tab
dos.configure(background='#010F57')
dosbg = ttk.Style
dostable = ttk.Treeview(dos, columns=("Date", "Subject", "Analysis", "Response"), show="headings")
logotable = ttk.Treeview(logo, columns=("Logo", "Subject", "Analysis", "Response"), show="headings")
urltable = ttk.Treeview(url, columns=("Email", "Subject", "Source", "Response"), show="headings")
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

# Function to update the history table with result data
def update_history_table(data):
    hist_table.delete(*hist_table.get_children())  # Clear existing table entries
    
    for i, entry in enumerate(data):
        date = entry['date']
        subject = entry['subject']
        analysis= entry['analysis']
        response = entry['response']
        
        hist_table.insert(parent="", index=i, iid=i, text="Row ",
                     values=(date, subject, analysis, response))

# Read user's email from user.json
with open('user.json', 'r') as file:
    user_info = json.load(file)
    email = user_info['email']
    
def save_to_database(dostable, urltable, logotable):
    result_data = []

    # Process dos table data
    dos_items = dostable.get_children()
    for item in dos_items:
        values = dostable.item(item)['values']
        date = values[0]
        subject = values[1]
        analysis = values[2]
        response = values[3]

        result_data.append({
            'date': date,
            'subject': subject,
            'analysis': analysis,
            'response': response
        })

    # Process url table data
    url_items = urltable.get_children()
    for item in url_items:
        values = urltable.item(item)['values']
        date = values[0]
        subject = values[1]
        analysis = values[2]
        response = values[3]

        result_data.append({
            'date': date,
            'subject': subject,
            'analysis': analysis,
            'response': response
        })

    # Process logo table data
    logo_items = logotable.get_children()
    for item in logo_items:
        values = logotable.item(item)['values']
        date = values[0]
        subject = values[1]
        analysis = values[2]
        response = values[3]

        result_data.append({
            'date': date,
            'subject': subject,
            'analysis': analysis,
            'response': response
        })

   # Save the result data to the database with a single push ID
    #database.child('Results').child(email.replace('.', '_')).push(result_data)

    
    # Update the history table with the saved data
    update_history_table(result_data)



# History Tab
hist.configure(background='#010F57')
bg = ttk.Style
hist_table = ttk.Treeview(hist, columns=("Details", "Subject", "Analysis", "Response"), show="headings")
# table.pack()

# Constructing vertical scrollbar with treeview
histtableverscrlbar = ttk.Scrollbar(hist, orient="vertical", command=hist_table.yview)

# Constructing horizontal scrollbar with treeview
histtablehorscrlbar = ttk.Scrollbar(hist, orient="horizontal", command=hist_table.xview)

# Configuring treeview
hist_table.configure(xscrollcommand=histtablehorscrlbar.set, yscrollcommand=histtableverscrlbar.set)
hist_table.heading("Details", text="Details", anchor="center")
hist_table.heading("Subject", text="Subject", anchor="center")
hist_table.heading("Analysis", text="Analysis", anchor="center")
hist_table.heading("Response", text="Response", anchor="center")
hist_table.column("Details", minwidth=240, anchor="w")
hist_table.column("Subject", width=510, anchor="w")
hist_table.column("Analysis", width=130, anchor="w")
hist_table.column("Response", width=400, anchor="w")

# Place treeview and scrollbars
hist_table.place(x=0, y=1, width=1513, height=752)  # Adjust these values as needed
histtableverscrlbar.place(x=1513, y=0, width=20, height=755)  # Adjust these values as needed
#histtablehorscrlbar.place(x=0, y=445, width=877, height=20)  # Adjust these values as needed

def update_chart(urltable, dostable, logotable):
    items_phish = urltable.get_children()  # Get all items in urltable
    total_phish = len(items_phish)
    flagged_phish = 0

    items_spam = dostable.get_children()  # Get all items in dostable
    total_spam = len(items_spam)
    flagged_spam = 0

    items_logo = logotable.get_children() # Get all items in logotable
    total_logo = len(items_logo)
    flagged_logo = 0

    for item in items_phish:
        analysis = urltable.item(item)['values'][2]
        if analysis == "Medium Risk for Phishing" or analysis == "High Risk for Phishing":
            flagged_phish += 1

    for item in items_spam:
        analysis = dostable.item(item)['values'][2]
        if analysis == "Medium Risk for Spam":
            flagged_spam += 1

    for item in items_logo:
        analysis = logotable.item(item)['values'][2]
        if analysis == "Possible Phishing":
            flagged_logo += 1

    not_flagged_phish = total_phish - flagged_phish
    not_flagged_spam = total_spam - flagged_spam
    not_flagged_logo = total_logo - flagged_logo
    flagged_emails = flagged_phish + not_flagged_logo + flagged_spam
    normal_emails = not_flagged_phish + not_flagged_spam + flagged_logo
    total_emails = total_spam + total_phish + total_logo
    percentages = {
        "Phishing": (flagged_phish + not_flagged_logo) / total_emails * 100,
        "Spam": flagged_spam / total_emails * 100,
        "Normal": (not_flagged_phish + not_flagged_spam + flagged_logo) / total_emails * 100
    }

    # Create a new figure with two subplots
    fig = Figure(figsize=(12, 4), dpi=100)
    ax1 = fig.add_subplot(121)  # Bar chart
    ax2 = fig.add_subplot(122)  # Existing chart

    # Define a visually appealing color palette
    colors = sns.color_palette("Set2")

    # Bar chart
    categories = percentages.keys()
    values = percentages.values()
    x_pos = np.arange(len(categories))
    ax1.bar(x_pos, values, align='center', alpha=0.8, color=colors)
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(categories)
    ax1.set_ylabel('Percentage')
    ax1.spines['top'].set_visible(False)  # Hide the top spine
    ax1.spines['right'].set_visible(False)  # Hide the right spine
    ax1.grid(axis='y', linestyle='--', alpha=0.5)  # Add dashed gridlines

    # Existing chart
    existing_labels = [''] * len(percentages)  # Add percentage labels
    ax2.pie(percentages.values(), labels=existing_labels, colors=colors, shadow=True, explode=(0.1, 0.1, 0.1), autopct='%1.1f%%', startangle=90)
    ax2.set_title("")
    ax2.axis('equal')  # Ensure pie is drawn as a circle

    # Set a common label for both charts
    fig.text(0.5, 0.94, 'Email Categories', ha='center', fontsize=14, weight='bold')

    canvas = FigureCanvasTkAgg(fig, master=chart)
    canvas.get_tk_widget().pack(pady=10, padx=20)

    canvas.draw()

    f1 = Frame(chart, width=300, height=300, bg='#85CEB7')
    f1.place(x=165, y=435)

    # Create a label to display the flagged emails count
    flagged_emails_label = Label(f1, text=f"Flagged Emails(Phishing&Spam):", font=("Arial", 12, "bold"), bg='#85CEB7', fg = 'white')
    flagged_emails_label.place(y=5)

    femails_label = Label(f1, text=f"{flagged_emails}", font=("Arial", 25, "bold"), bg='#85CEB7', fg = 'white')
    femails_label.place(relx=0.5, rely=0.5, anchor='center')

    f2 = Frame(chart, width=300, height=300, bg='#FBA481')
    f2.place(x=620, y=435)

    # Create a label to display the normal emails count
    normal_emails_label = Label(f2, text="Normal Emails:", font=("Arial", 12, "bold"), bg='#FBA481', fg = 'white')
    normal_emails_label.place(y=5)

    nemails_label = Label(f2, text=f"{normal_emails}", font=("Arial", 25, "bold"), bg='#FBA481', fg = 'white')
    nemails_label.place(relx=0.5, rely=0.5, anchor='center')

    f3 = Frame(chart, width=300, height=300, bg='#A4B2D3')
    f3.place(x=1065, y=435)

    # Create a label to display the Total emails count
    total_emails_label = Label(f3, text="Total Emails:", font=("Arial", 12, "bold"), bg='#A4B2D3', fg = 'white')
    total_emails_label.place(y=5)

    tmails_label = Label(f3, text=f"{total_emails}", font=("Arial", 25, "bold"), bg='#A4B2D3', fg = 'white')
    tmails_label.place(relx=0.5, rely=0.5, anchor='center')

emcbg = ttk.Style
emctable = ttk.Treeview(em_c, columns=("Date", "Subject", "Analysis", "Response"), show="headings")
# table.pack()

# Constructing vertical scrollbar with treeview
emctableverscrlbar = ttk.Scrollbar(em_c, orient="vertical", command=emctable.yview)

# Constructing horizontal scrollbar with treeview
emctablehorscrlbar = ttk.Scrollbar(em_c, orient="horizontal", command=emctable.xview)

# Configuring treeview
emctable.configure(xscrollcommand=emctablehorscrlbar.set, yscrollcommand=emctableverscrlbar.set)

emctable.heading("Date", text="Details", anchor="center")
emctable.heading("Subject", text="Subject", anchor="center")
emctable.heading("Analysis", text="Analysis", anchor="center")
emctable.heading("Response", text="Response", anchor="center")
emctable.column("Date", minwidth=240, anchor="w")
emctable.column("Subject", width=710, anchor="w")
emctable.column("Analysis", width=130, anchor="w")
emctable.column("Response", width=450, anchor="w")

# Place treeview and scrollbars
emctable.place(x=0, y=1, width=1513, height=752)  # Adjust these values as needed
emctableverscrlbar.place(x=1513, y=0, width=20, height=755)  # Adjust these values as needed
#emctablehorscrlbar.place(x=0, y=735, width=1513, height=20)  # Adjust these values as needed


urlbg = ttk.Style
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
    urltable.heading("Email", text="Email", anchor="center")
    urltable.heading("Subject", text="Subject", anchor="center")
    urltable.heading("Source", text="Analysis", anchor="center")
    urltable.heading("Response", text="Response", anchor="center")
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
                score = 0
                if domainString == 'gmail.com' or domainString == "yahoo.com":
                    messageforurl = "Medium Risk for Phishing"
                    explanationforurl = "The email of the sender is a personal email."
                    score = 12
                else:
                    indexOfLessThan = fromStringValue.find('<')
                    if indexOfLessThan == -1:
                        emailString = fromStringValue
                        messageforurl = "Low Risk for Phishing"
                        explanationforurl = "The sender's email is a legitimate email associated with their institution."
                        score = 25
                    else:
                        score = 25
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
                #             messageforurl = "High Risk for Phishing"
                #             explanationforurl = "The sender's email is disposable"
                #             score = 0
                #         else:
                #             messageforurl = "The sender's email looks legitimate."
                #             score = 25
                totalMessages.append(personalMessages[i])
                urltable.insert(parent="", index=i, iid=i, text=personalMessages[i]["id"],
                                values=(emailString, personalMessages[i]["snippet"], messageforurl, explanationforurl))
                # emctable.insert(parent="", index=len(totalMessages), iid=len(totalMessages), text=personalMessages[i]["id"],
                #                 values=(emailString, personalMessages[i]["snippet"], messageforurl, explanationforurl))
                summarydictionary[personalMessages[i]["id"]]["totalscore"] = summarydictionary[personalMessages[i]["id"]]["totalscore"] + 25
                summarydictionary[personalMessages[i]["id"]]["score"] = summarydictionary[personalMessages[i]["id"]]["score"] + score
                emctable.insert(parent="", index=i, iid=i, text=personalMessages[i]["id"],
                                values=(emailString, personalMessages[i]["snippet"], str(summarydictionary[personalMessages[i]["id"]]["score"]) + "/" + str(summarydictionary[personalMessages[i]["id"]]["totalscore"]), explanationforurl))
                #hist_table.insert(parent="", index=i + len(personalMessages), iid=i + len(personalMessages), text=personalMessages[i]["id"],
                                #values=(emailString, personalMessages[i]["snippet"], messageforurl, explanationforurl))
    
                urltable.column("Email", minwidth=240, anchor="w")
                urltable.column("Subject", width=515, anchor="w")
                urltable.column("Source", width=120, anchor="w")
                urltable.column("Response", width=450, anchor="w")
                urltable.bind('<Button-1>', selectItem)


    # Place treeview and scrollbars
    urltable.place(x=0, y=1, width=1513, height=752)  # Adjust these values as needed
    urltableverscrlbar.place(x=1513, y=0, width=20, height=755)  # Adjust these values as needed
    #urltablehorscrlbar.place(x=0, y=445, width=877, height=20)  # Adjust these values as needed
    update_chart(urltable, dostable, logotable)
    save_to_database(dostable, logotable, urltable)

checkboxvariable = IntVar()


checkbox = Checkbutton(result, text = "Improve our database by including your trashed data", variable = checkboxvariable,
                 onvalue = 1, offvalue = 0, height=1,
                 width = 50)
checkbox.place(x=500, y=15)


def callback():
    indexSelected = notebook.index(notebook.select())
    if indexSelected == 0:
        if emctable.focus() != '':
            indexToBeDeleted = int(emctable.focus())
            delete(totalMessages[indexToBeDeleted])
    elif indexSelected == 1:
        if emctable.focus() != '':
            indexToBeDeleted = int(emctable.focus())
            # delete(totalMessages[indexToBeDeleted])
    else:
        print("")



def todash():
    result.destroy()
    os.system("Dashboard.py")

spamButton = Button(result, text="Move to trash", command=callback)
spamButton.place(x=1000, y=15)

bck_btn = Button(result, text="Return to dashboard", command=todash)
bck_btn.place(x=1400, y=15)

# Exit Button
result.after(0, gotoscreens)
result.mainloop()
