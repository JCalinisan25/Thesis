from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import pymysql
import os

# window
regist = Tk()
regist.title("Registration Page")
regist.geometry("700x400")


def tosign():
    regist.destroy()
    os.system('Login.py')


def toterms():
    regist.destroy()
    os.system('TermsnCond.py')


def inval():
    if user.get() == '' and email.get() == '' and passw.get() == '':
        messagebox.showerror("Error", "No Input in the field!")
    elif user.get() == '' or email.get() == '' or passw.get() == '':
        messagebox.showerror("Error", "No Input in other field!")
    else:
        try:
            con=pymysql.connect(host='localhost', user='root', password='Pangthesis2023@', database='EPBIP')
            cur=con.cursor()
            cur.execute('select * from register where emailid=%s', email.get())
            row=cur.fetchone()
            if row!=None:
                messagebox.showerror("Error", "User already Exist, Please try with another Email!")
            else:
                cur.execute("insert into register values(%s,%s,%s)",(user.get(), email.get(), passw.get()))
                con.commit()
                con.close()
                messagebox.showinfo("Success", "Register Successfully!")
                regist.destroy()
                os.system('EmailVerif.py')
        except Exception as es:
            messagebox.showerror("Error",f'Error Due to : {str(es)}')


# Background
bg_0 = Image.open("img\\bg.jpg")
bck_pk = ImageTk.PhotoImage(bg_0.resize((700, 400)))

lbl = Label(regist, image=bck_pk, border=0)
lbl.place(x=1, y=1)

# Header
box_1 = Frame(regist, width=700, height=55, bg='#010F57')
box_1.place(x=3, y=5)
heading = Label(regist, text='REGISTER', fg='white', bg='#010F57', font=('Arial', 30, 'bold'))
heading.place(x=250, y=5)

# logo
box_2 = Frame(regist, width=555, height=290, bg='#010F57')
box_2.place(x=70, y=80)

logo = Image.open("img\\logoo.png")
log_pk = ImageTk.PhotoImage(logo.resize((210, 205)))

lbl = Label(box_2, image=log_pk, border=0)
lbl.place(x=5, y=15)

log_name = Label(box_2, text='E.P.B.I.P', fg='white', bg='#010F57', font=('Copperplate', 30, 'bold'))
log_name.place(x=30, y=220)

username = StringVar()
emails = StringVar()
password = StringVar()

# user
user_name = Label(box_2, text='Username:', fg='white', bg='#010F57', font=('Arial', 17, 'bold'))
user_name.place(x=225, y=23)
user = Entry(box_2, textvariable=username, width=23, fg='black', border=1, bg='white', font=('Arial', 11, 'bold'))
user.place(x=350, y=27)

# email
email_name = Label(box_2, text='Email Add.:', fg='white', bg='#010F57', font=('Arial', 18, 'bold'))
email_name.place(x=212, y=70)
email = Entry(box_2, textvariable=emails, width=23, fg='black', border=1, bg='white', font=('Arial', 11, 'bold'))
email.place(x=350, y=75)

# password
pass_name = Label(box_2, text='Password:', fg='white', bg='#010F57', font=('Arial', 18, 'bold'))
pass_name.place(x=224, y=119)
passw = Entry(box_2, textvariable=password, width=23, fg='black', border=1, bg='white', font=('Arial', 11, 'bold'),
              show="*")
passw.place(x=350, y=123)

# button
Button(box_2, width=9, pady=6, text="Register", bg='white', cursor='hand2', font=('Arial', 12, 'bold'),
       command=inval).place(x=300, y=175)

Button(box_2, width=10, pady=6, text="Login", bg='white', cursor='hand2', font=('Arial', 12, 'bold'),
       command=tosign).place(x=410, y=175)


# Terms and Conditions/DPA Acceptance
check = Checkbutton(regist, fg='black', onvalue=1, offvalue=0, bg='#010F57', font=('Arial', 8, 'bold'))
check.place(x=325, y=320)

text1 = Label(box_2, text="I agree to E.P.B.I.P", fg='white', bg='#010F57', font=('Arial', 8, 'bold'))
text1.place(x=280, y=242)

trm = Button(box_2, width=17, text='terms and conditions', border=0, bg='#010F57', cursor='hand2', fg='#38B6FF',
             font=('Arial', 8, 'bold', 'underline'), command=toterms)
trm.place(x=377, y=242)

text2 = Label(box_2, text="and ", fg='white', bg='#010F57', font=('Arial', 8, 'bold'))
text2.place(x=497, y=242)

dpa = Button(box_2, width=14, text='Privacy Policy', border=0, bg='#010F57', cursor='hand2', fg='#38B6FF',
             font=('Arial', 8, 'bold', 'underline'), command=toterms)
dpa.place(x=268, y=258)

regist.mainloop()
