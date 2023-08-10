from tkinter import Tk, Frame, Button, Label
from PIL import Image, ImageTk
import customtkinter as ctk
import os



# Window
vefy = Tk()
vefy.title("E.P.B.I.P")
vefy.geometry("400x400")
vefy.resizable(False, False)
vefy.iconbitmap(r'img\\logo.ico')

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
center_window(vefy)

def log():
    vefy.destroy()
    os.system("Login.py")

# Background
bg_0 = Image.open("img\\bg8.jpg")
bck_pk = ImageTk.PhotoImage(bg_0.resize((400, 400)))

lbl = Label(vefy, image=bck_pk, border=0)
lbl.place(x=1, y=1)

# Box with rounded corners
box_1 = Frame(vefy, width=370, height=355, bg='#010F57')
box_1.place(x=15, y=20)

# Logo
logo = Image.open("img\\logoo.png")
log_pk = ImageTk.PhotoImage(logo.resize((165, 160)))

lbl = Label(box_1, image=log_pk, border=0)
lbl.place(x=105, y=2)

log_name = Label(box_1, text='Please Verify Your Email', fg='white', bg='#010F57', font=('Copperplate', 15, 'bold'))
log_name.place(x=65, y=180)


info = Label(box_1, text= f"We've sent a verification link to your email.\nPlease check your email to verify your " \
             "email address \nand activate your account.", fg='white', bg='#010F57', font=('Arial', 10, 'bold'), justify='center')
info.place(x=15, y=220)

# Button
check = Image.open("img/check.png")
check_pk = ImageTk.PhotoImage(check.resize((30, 25)))

lbl = Label( image=check_pk)

btn = Button(box_1, image=check_pk, bg="#1A6BA6",command=log, bd=0, activebackground='#174D74', width=80)
btn.place(x=150, y=300)


vefy.mainloop()