from tkinter import *
from PIL import Image, ImageTk


def toreg():
    terms.destroy()
    import Registration


# window
terms = Tk()
terms.title("Terms and Conditions Page")
terms.geometry("600x700")

# Background
bg_0 = Image.open("D:\\Codes\\Python\\Thesis\\img\\bg.jpg")
bck_pk = ImageTk.PhotoImage(bg_0.resize((600, 700)))

lbl = Label(terms, image=bck_pk)
lbl.place(x=1, y=1)

# content
box_1 = Frame(terms, width=560, height=660, bg='#010F57')
box_1.place(x=20, y=20)

Button(box_1, text="X", fg='white', width=1, height=0, bg='#010F57', font=('Arial', 10, 'bold'), bd=0,
       command=toreg).place(x=539, y=5)

text_lbl = Label(box_1, text="TERMS AND CONDITIONS", font=('Arial', 17, 'bold'), bg='#010F57', fg='white')
text_lbl.place(x=133, y=7)

terms.mainloop()
