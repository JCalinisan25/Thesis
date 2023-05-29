from tkinter import *
from PIL import Image, ImageTk

# Window
vefy = Tk()
vefy.title("Verification Page")
vefy.geometry("500x400")

def log():
    vefy.destroy()
    import Login


# Background
bg_0 = Image.open("img\\bg.jpg")
bck_pk = ImageTk.PhotoImage(bg_0.resize((500, 400)))

lbl = Label(vefy, image=bck_pk, border=0)
lbl.place(x=1, y=1)

# Box
box_1 = Frame(vefy, width=470, height=355, bg='#010F57')
box_1.place(x=15, y=20)

# Logo
logo = Image.open("img\\logoo.png")
log_pk = ImageTk.PhotoImage(logo.resize((165, 160)))

lbl = Label(box_1, image=log_pk, border=0)
lbl.place(x=150, y=5)

log_name = Label(box_1, text='E.P.B.I.P', fg='white', bg='#010F57', font=('Copperplate', 35, 'bold'))
log_name.place(x=140, y=160)

info = Label(box_1, text="Please check your email for verification.\nThank you for using our application. Have a great day.",
             fg='white', bg='#010F57', font=('Arial', 10, 'bold'))
info.place(x=70, y=230)

# Button
btn = Button(box_1, width=10, pady=5, text="Go back", bg='white', fg='black', cursor='hand2', border=0,
             font=('Arial', 12, 'bold'), command=log)
btn.place(x=185, y=290)

vefy.mainloop()
