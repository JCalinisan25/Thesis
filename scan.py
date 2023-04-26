from tkinter import *
from tkinter import ttk
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk
from tkinter import messagebox
import os

# window
scan = Tk()
scan.title("Scanning Page")
scan.geometry("450x450")


def tosign():
    scan.destroy()
    os.system('Login.py')


# Background
bg_0 = Image.open("D:\\Codes\\Python\\Thesis\\img\\bg.jpg")
bck_pk = ImageTk.PhotoImage(bg_0.resize((450, 450)))

lbl = Label(scan, image=bck_pk, border=0)
lbl.place(x=1, y=1)

# Header
box_1 = Frame(scan, width=500, height=55, bg='#010F57')
box_1.place(x=3, y=5)
heading = Label(scan, text='DASHBOARD', fg='white', bg='#010F57', font=('Arial', 30, 'bold'))
heading.place(x=100, y=5)

# profile
box_2 = Frame(scan, width=390, height=350, bg='#010F57')
box_2.place(x=30, y=80)

person = Image.open("D:\\Codes\\Python\\Thesis\\img\\person.JPG")
per_pk = ImageTk.PhotoImage(person.resize((105, 110)))

lbl = Label(box_2, image=per_pk, border=0)
lbl.place(x=10, y=5)

edit = Image.open("D:\\Codes\\Python\\Thesis\\img\\edit.PNG")
ed_pk = ImageTk.PhotoImage(edit.resize((18, 18)))

lbl = Label(scan, image=ed_pk, border=0)
lbl.place(x=35, y=191)

user = Label(box_2, text='Username', fg='white', bg='#010F57', font=('Arial', 11, 'bold'))
user.place(x=20, y=110)

# logout
log = Image.open("D:\\Codes\\Python\\Thesis\\img\\logout.JPG")
lg_pk = ImageTk.PhotoImage(log.resize((30, 25)))

lbl = Label(scan, image=lg_pk, border=0)
lbl.place(x=300, y=91)

lg_btn = Button(box_2, bg="#010F57", bd=0, height=1, width=9, text="   Logout", fg='white', font=('Arial', 15, 'bold'),
                cursor='hand2', command=tosign)
lg_btn.place(x=270, y=5)

# To scan
progress_label = Label(box_2, text="Scanning...", font=('Arial', 15, 'bold'), fg='white', bg="#010F57")
progress_label.place(x=30, y=200)

progress = ttk.Style()
progress.theme_use('clam')
progress.configure("red.Horizontal.TProgressbar", bg='#010F57')

progress = Progressbar(box_2, orient=HORIZONTAL, length=330, mode='determinate', style="red.Horizontal.TProgressbar")
progress.place(x=30, y=240)


def top():
    messagebox.showinfo("Scan", "Scan Successfully!")
    scan.destroy()
    os.system("Dashboard.py")


i = 0


def load():
    global i
    if i <= 50:
        txt = 'Scanning... ' + (str(2 * i) + '%')
        progress_label.config(text=txt)
        progress_label.after(100, load)
        progress['value'] = 2 * i
        i += 1

    else:
        top()


load()
scan.mainloop()
