from tkinter import *
from PIL import Image, ImageTk
import os

# window
verify = Tk()
verify.title("Verification Page")
verify.geometry("500x400")


def vfied():
            verify.destroy()
            os.system('Verified.py')




# Background
bg_0 = Image.open("img\\bg.jpg")
bck_pk = ImageTk.PhotoImage(bg_0.resize((500, 400)))

lbl = Label(verify, image=bck_pk, border=0)
lbl.place(x=1, y=1)

# box
box_1 = Frame(verify, width=470, height=355, bg='#010F57')
box_1.place(x=15, y=20)

# logo
logo = Image.open("img\\logoo.png")
log_pk = ImageTk.PhotoImage(logo.resize((95, 90)))

lbl = Label(box_1, image=log_pk, border=0)
lbl.place(x=200, y=1)

log_name = Label(box_1, text='E.P.B.I.P', fg='white', bg='#010F57', font=('Copperplate', 18, 'bold'))
log_name.place(x=200, y=90)

box_2 = Frame(box_1, width=470, height=3, bg='white')
box_2.place(x=1, y=133)

heading = Label(box_1, text='Verify Your Account', fg='white', bg='#010F57', font=('Arial', 25, 'bold'))
heading.place(x=90, y=140)

info = Label(box_1, text="Welcome to E.P.B.I.P, Before we get \nstarted, please confirm your email address.",
             fg='white', bg='#010F57', font=('Arial', 14, 'bold'))
info.place(x=15, y=190)

info = Label(box_1, text="Thankyou, \nSoftyware Team", fg='white', bg='#010F57', font=('Arial', 14, 'bold'))
info.place(x=20, y=300)

# button
Button(box_1, width=10, pady=5, text="Verify!", bg='#355E3B', fg='white', cursor='hand2', border=0,
       font=('Arial', 12, 'bold'), command=vfied).place(x=200, y=265)

verify.mainloop()
