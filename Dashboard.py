from tkinter import Tk, Label, Frame, Button, PhotoImage
from PIL import Image, ImageTk, ImageDraw
from tkinter import messagebox, filedialog
import os, pyrebase, json, webbrowser

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
json_file_path = "token.json"


def tosign():
    msg = messagebox.askyesno('Logout', 'Are you sure you want to logout?')
    if msg:
        # Check if the "token.json" file exists
        if os.path.exists('token.json'):
            os.remove('token.json')
        
        with open('user.json', 'w') as file:
            json.dump({}, file)
        
        dash.destroy()
        os.system('Login.py')

# window
dash = Tk()
dash.title("E.P.B.I.P")
dash.geometry("450x450")
dash.resizable(False, False)
dash.iconbitmap(r'img\\logo.ico')

# Function to center the tkinter window
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
center_window(dash)

def toscan():
    dash.destroy()
    os.system('scan.py')

def home():
    if 'f4' in globals():
        f4.destroy()
    
    global box_2
    box_2 = Frame(dash, width=415, height=415, bg='#010F57')
    box_2.place(x=20, y=20)

    brgr_btn = Button(box_2, bg="#010F57", bd=0, height=40, width=30, image=brgr_pk, cursor='hand2', command=toggle_menu,
                    activebackground='#010F57')
    brgr_btn.place(x=10, y=5)

    lbl2 = Label(box_2, bg='#010F57',image=logo_pk)
    lbl2.place(x=150, y=10)

    username = Label(box_2, text=username_label_text, fg='white', bg='#010F57', font=('Arial', 25, 'bold'))
    username.place(x=100, y=120)

    lg_btn = Button(box_2, bg="#010F57", bd=0, height=40, width=30, image=lg_pk, cursor='hand2', command=tosign,
                    activebackground="#010F57")
    lg_btn.place(x=370, y=5)

    sc_btn = Button(box_2, image=scan_btn, width=300, height=90, bg="#021976", bd=0, cursor='hand2', command=toscan)
    sc_btn.place(x=50, y=170)

    rp_btn = Button(box_2, image=rep_btn, width=300, height=90, bg="#021976", bd=0, cursor='hand2', command=toresult)
    rp_btn.place(x=50, y=280)

def guide():
    f1.destroy()
    pdf_file = "EPBIP_Guide-v1.1.pdf"
    webbrowser.open(pdf_file)

def manual():
    f1.destroy()
    pdf_file = "E.P.B.I.P_User_Manual.pdf"
    webbrowser.open(pdf_file)
   
def about():
    global f4
    f1.destroy()
    f4 = Frame(box_2, width=415, height=515, bg='#010F57')
    f4.place(x=0, y=0)
    brgr_btn = Button(f4, bg="#010F57", bd=0, height=40, width=30, image=brgr_pk, cursor='hand2', command=toggle_menu)
    brgr_btn.place(x=10, y=5)

    about_text = """

    At EPBIP, we utilize Backtracking and Image Processing algorithms to protect users from email phishing and spam attacks. Our sophisticated application analyzes content and attachments and examines images to detect suspicious patterns and visual manipulations. With a user-friendly interface and continuous improvement, we provide robust protection against evolving cyber threats, ensuring the security of sensitive information in email communications. Trust EPBIP for email security simplified.
    """

    about_label = Label(f4, text=about_text, bg='#010F57', fg='white', justify='left', font=('Arial', 12), wraplength=390)
    about_label.pack(pady=90, padx=20)

    about_title_label = Label(f4, text="About Us", bg='#010F57', fg='white', font=('Arial', 24, 'bold', 'underline'))
    about_title_label.place(x=140,y=40)

def toggle_menu():
    global f1
    f1=Frame(box_2,width=180,height=400,bg='#021976')
    f1.place(x=5,y=5)
    l0=Frame(f1,width=146,height=2,bg='white')
    l0.place(x=0,y=82)
    l1=Frame(f1,width=146,height=2,bg='white')
    l1.place(x=0,y=122)
    l2=Frame(f1,width=146,height=2,bg='white')
    l2.place(x=0,y=162)
    l3=Frame(f1,width=146,height=2,bg='white')
    l3.place(x=0,y=389)

    #buttons
    def bttn(x,y,text,bcolor,fcolor,cmd):
     
        def on_entera(e):
            myButton1['background'] = bcolor #ffcc66
            myButton1['foreground']= 'white'  #000d33

        def on_leavea(e):
            myButton1['background'] = fcolor
            myButton1['foreground']= 'white'

        myButton1 = Button(f1,text=text,
                    width=20,
                    height=2,
                    fg='white',
                    border=0,
                    bg=fcolor,
                    activeforeground='white',
                    activebackground=bcolor,
                    font=('Arial', 9, 'bold'),           
                    command=cmd)
                      
        myButton1.bind("<Enter>", on_entera)
        myButton1.bind("<Leave>", on_leavea)

        myButton1.place(x=x,y=y)

    bttn(0,45,'Home','#0f9d9a','#021976',home)
    bttn(0,85,'User Guide','#0f9d9a','#021976',guide)
    bttn(0,125,'User Manual','#0f9d9a','#021976',manual)
    bttn(0,350,'About Us','#0f9d9a','#021976',about)

    #exit
    def dele():
        f1.destroy()

    close = Button(f1, bg="#021976", bd=0, height=1, width=1, text="X", fg='white', font=('Arial', 15, 'bold'),
                cursor='hand2', command=dele, activebackground='#010F57', activeforeground='white')
    close.place(x=5, y=1)

def toresult():
    # Check if the sc_btn is clicked
    if os.path.exists(json_file_path):
        dash.destroy()
        os.system('Results.py')
            
    else:
        messagebox.showinfo("No Scan", "No data found.Please scan your email first.")

# Background
bg_0 = Image.open("img\\bg8.jpg")
bck_pk = ImageTk.PhotoImage(bg_0.resize((450, 450)))

lbl1 = Label(dash, image=bck_pk, border=0)
lbl1.place(x=1, y=1)


# profile
box_2 = Frame(dash, width=415, height=415, bg='#010F57')
box_2.place(x=20, y=20)

logo = Image.open("img\\logoo.png")
logo_pk = ImageTk.PhotoImage(logo.resize((105, 105)))

lbl2 = Label(box_2, bg='#010F57',image=logo_pk)
lbl2.place(x=150, y=10)
 
brgr = Image.open("img\\hamburger.png")
brgr_pk = ImageTk.PhotoImage(brgr.resize((35, 35)))

lbl3 = Label( image=brgr_pk)

brgr_btn = Button(box_2, bg="#010F57", bd=0, height=40, width=30, image=brgr_pk, cursor='hand2', command=toggle_menu,
                activebackground='#010F57')
brgr_btn.place(x=10, y=5)

# Get the email from the login process
try:
    with open('user.json', 'r') as file:
        user_info = json.load(file)
        email = user_info['email']
except FileNotFoundError:
        messagebox.showerror("Error", "No user is signed in!")
        email = ""

# Retrieve username from Firebase Realtime Database based on the email
users = database.child("Users").get()
username = "username"
for user in users.each(): # type: ignore
    if user.val()['email'] == email:
        username = user.val()['username']
        break

username_label_text = f"Hi, {username}"
username_length = len(username)

x_pos = (415 - (30 * username_length)) // 2

user = Label(box_2, text=username_label_text, fg='white', bg='#010F57', font=('Arial', 25, 'bold'))
user.place(x=x_pos, y=120)

# logout
log = Image.open("img\\logout.JPG")
lg_pk = ImageTk.PhotoImage(log.resize((30, 25)))

lbl4 = Label( image=lg_pk)

lg_btn = Button(box_2, bg="#010F57", bd=0, height=40, width=30, image=lg_pk, cursor='hand2', command=tosign,
                    activebackground='#010F57')
lg_btn.place(x=370, y=5)

# To scan
scan_btn = PhotoImage(file='img\\scan.png')
sc_label = Label(image=scan_btn)

sc_btn = Button(box_2, image=scan_btn, width=300, height=90, bg="#021976", bd=0, cursor='hand2', command=toscan)
sc_btn.place(x=50, y=170)

# To results
rep_btn = PhotoImage(file="img\\det.png")
rp_label = Label(image=rep_btn)

rp_btn = Button(box_2, image=rep_btn, width=300, height=90, bg="#021976", bd=0, cursor='hand2', command=toresult)
rp_btn.place(x=50, y=280)

dash.mainloop()