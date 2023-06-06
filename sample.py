from tkinter import *
from PIL import Image, ImageTk, ImageDraw
from tkinter import messagebox, filedialog
import os, pyrebase, json

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

def tosign():
    dash.destroy()
    os.system('Login.py')

def toresult():
    dash.destroy()
    os.system('Results.py')

def toscan():
    dash.destroy()
    os.system('scan.py')

def home():
    if 'f2' in globals():
        f2.destroy()
    elif 'f3' in globals():
        f3.destroy()
    elif 'f4' in globals():
        f4.destroy()

    global box_2
    box_2 = Frame(dash, width=415, height=415, bg='#010F57')
    box_2.place(x=20, y=20)

    lbl = Label(box_2, image=per_pk, border=0)
    lbl.place(x=160, y=15)

    brgr_btn = Button(box_2, bg="#010F57", bd=0, height=40, width=30, image=brgr_pk, cursor='hand2', command=toggle_menu)
    brgr_btn.place(x=10, y=5)

    username = Label(box_2, text=username_label_text, fg='white', bg='#010F57', font=('Arial', 15, 'bold'))
    username.place(x=150, y=120)

    lg_btn = Button(box_2, bg="#010F57", bd=0, height=40, width=30, image=lg_pk, cursor='hand2', command=tosign)
    lg_btn.place(x=370, y=5)

    sc_btn = Button(box_2, image=scan_btn, width=300, height=90, bg="#021976", bd=0, cursor='hand2', command=toscan)
    sc_btn.place(x=50, y=170)

    rp_btn = Button(box_2, image=rep_btn, width=300, height=90, bg="#021976", bd=0, cursor='hand2', command=toresult)
    rp_btn.place(x=50, y=280)


def profile():
    global f2, profile_image
    f1.destroy()
    f2 = Frame(box_2, width=415, height=415, bg='#010F57')
    f2.place(x=0, y=0)
    brgr_btn = Button(f2, bg="#010F57", bd=0, height=40, width=30, image=brgr_pk, cursor='hand2', command=toggle_menu)
    brgr_btn.place(x=10, y=5)

    def exit():
        f2.destroy()
        home()

    close = Button(f2, bg="#010F57", bd=0, height=1, width=1, text="X", fg='white', font=('Arial', 15, 'bold'),
                   cursor='hand2', command=exit)
    close.place(x=390, y=5)

    # Select and display image
    # Select and display image
    def select_image():
        global profile_image
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            profile_image = Image.open(file_path)
            profile_image = profile_image.resize((95, 100))
        
        # Create a circular mask
            mask = Image.new("L", (95, 100), 255)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, 95, 100), fill=255)
        
        # Apply the circular mask to the image
            profile_image = ImageTk.PhotoImage(Image.composite(profile_image, Image.new("RGB", profile_image.size, (1, 15, 87, 0)), mask))
        
        # Configure the image for the profile_photo label
            profile_photo.config(image=profile_image)
            profile_photo.image = profile_image


    select_btn = Button(f2, text="Select Image", bg="#021976", fg="white", bd=0, cursor="hand2",
                        command=select_image, font=('Arial', 12, 'bold'))
    select_btn.place(x=180, y=140)

    profile_photo = Label(f2, image=per_pk, border=0)
    profile_photo.place(x=160, y=15)

    # Change username and password
    def change_credentials():
        """new_username = new_username_entry.get().strip()

        if new_username == "":
            messagebox.showerror("Error", "Please enter a new username.")
            return"""

        try:
            """user = auth.current_user  # Retrieve current user information
            # Change username
            database.child("Users").child(user["localId"]).update({"username": new_username})
            messagebox.showinfo("Success", "Username has been updated.")
            new_username_entry.delete(0, END)"""

            # Update the selected profile image
            if 'profile_image' in globals() and profile_image:
            # Display the selected profile image on the person label
                person_label.config(image=profile_image)
                person_label.image = profile_image
                messagebox.showinfo("Success", "Update Successully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    """# Username label and entry
    username_label = Label(f2, text="New Username:", fg='white', bg='#010F57', font=('Arial', 12, 'bold'))
    username_label.place(x=40, y=180)

    new_username_entry = Entry(f2, width=30)
    new_username_entry.place(x=180, y=180)
"""
    # Change credentials button
    change_credentials_btn = Button(f2, text="Update", width=15, bg="#021976", fg="white", bd=0, cursor="hand2",
                                    command=change_credentials, font=('Arial', 12, 'bold'))
    change_credentials_btn.place(x=180, y=220)


def manual():
    global f3
    f1.destroy()
    f3=Frame(box_2,width=415, height=415,bg='#010F57')
    f3.place(x=0, y=0)
    l3=Label(f3,text='Acer',fg='white',bg='white')
    l3.config(font=('Comic Sans MS',90))
    l3.place(x=290,y=150-45)
    brgr_btn = Button(f3, bg="#010F57", bd=0, height=40, width=30, image=brgr_pk, cursor='hand2', command=toggle_menu)
    brgr_btn.place(x=10, y=5)
   

def about():
    global f4
    f1.destroy()
    f4=Frame(box_2,width=415, height=415,bg='#010F57')
    f4.place(x=0, y=0)
    l4=Label(f4,text='Dell',fg='white',bg='white')
    l4.config(font=('Comic Sans MS',90))
    l4.place(x=320,y=150-45)
    brgr_btn = Button(f4, bg="#010F57", bd=0, height=40, width=30, image=brgr_pk, cursor='hand2', command=toggle_menu)
    brgr_btn.place(x=10, y=5)

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
    bttn(0,85,'Profile','#0f9d9a','#021976',profile)
    bttn(0,125,'User Manual','#0f9d9a','#021976',manual)
    bttn(0,350,'About Us','#0f9d9a','#021976',about)

    #exit
    def dele():
        f1.destroy()

    close = Button(f1, bg="#021976", bd=0, height=1, width=1, text="X", fg='white', font=('Arial', 15, 'bold'),
                cursor='hand2', command=dele)
    close.place(x=5, y=1)

# Background
bg_0 = Image.open("img\\bg8.jpg")
bck_pk = ImageTk.PhotoImage(bg_0.resize((450, 450)))

lbl1 = Label(dash, image=bck_pk, border=0)
lbl1.place(x=1, y=1)


# profile
box_2 = Frame(dash, width=415, height=415, bg='#010F57')
box_2.place(x=20, y=20)

person = Image.open("img\\person.JPG")
per_pk = ImageTk.PhotoImage(person.resize((95, 100)))

person_label = Label(box_2, image=per_pk, border=0)
person_label.place(x=160, y=15)

brgr = Image.open("img\\hamburger.png")
brgr_pk = ImageTk.PhotoImage(brgr.resize((35, 35)))

lbl3 = Label( image=brgr_pk)

brgr_btn = Button(box_2, bg="#010F57", bd=0, height=40, width=30, image=brgr_pk, cursor='hand2', command=toggle_menu)
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
for user in users.each():
    if user.val()['email'] == email:
        username = user.val()['username']
        break

username_label_text = f"Hi, {username}"
user = Label(box_2, text=username_label_text, fg='white', bg='#010F57', font=('Arial', 15, 'bold'))
user.place(x=150, y=120)

# logout
log = Image.open("img\\logout.JPG")
lg_pk = ImageTk.PhotoImage(log.resize((30, 25)))

lbl4 = Label( image=lg_pk)

lg_btn = Button(box_2, bg="#010F57", bd=0, height=40, width=30, image=lg_pk, cursor='hand2', command=tosign)
lg_btn.place(x=370, y=5)

# To scan
scan_btn = PhotoImage(file='img\scan.png')
sc_label = Label(image=scan_btn)

sc_btn = Button(box_2, image=scan_btn, width=300, height=90, bg="#021976", bd=0, cursor='hand2', command=toscan)
sc_btn.place(x=50, y=170)

# To results
rep_btn = PhotoImage(file="img\det.png")
rp_label = Label(image=rep_btn)

rp_btn = Button(box_2, image=rep_btn, width=300, height=90, bg="#021976", bd=0, cursor='hand2', command=toresult)
rp_btn.place(x=50, y=280)

dash.mainloop()
