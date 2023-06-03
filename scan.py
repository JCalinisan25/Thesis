from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import os, time

# window
scan = Tk()
scan.title("E.P.B.I.P")
scan.geometry("450x450")
scan.resizable(False, False)
scan.iconbitmap(r'img\\logo.ico')

# Flag to indicate whether to continue scanning or not
continue_scanning = True


def to_sign():
    global continue_scanning
    if messagebox.askyesno("Confirmation", "Are you sure you want to quit while scanning?"):
        continue_scanning = False
        scan.destroy()
        os.system('Dashboard.py')


def complete_scan():
    messagebox.showinfo("Successful", "Scan completed successfully!")
    scan.destroy()
    os.system('Results.py')


# Background
bg_0 = Image.open("img\\bg8.jpg")
bck_pk = ImageTk.PhotoImage(bg_0.resize((450, 450)))

lbl = Label(scan, image=bck_pk, border=0)
lbl.place(x=1, y=1)

# profile
box_2 = Frame(scan, width=390, height=390, bg='#010F57')
box_2.place(x=30, y=30)

# quit
lg_btn = Button(box_2, bg="#010F57", bd=0, height=1, width=1, text="X", fg='white', font=('Arial', 15, 'bold'),
                cursor='hand2', command=to_sign)
lg_btn.place(x=365, y=1)

# To scan
progress_label_text = StringVar()
progress_label_text.set("Scanning... 0%")
progress_label = Label(box_2, textvariable=progress_label_text, font=('Arial', 15, 'bold'), fg='white', bg="#010F57")
progress_label.place(x=30, y=250)

progress_bar_width = 325
progress_bar_height = 10
progress_bar_x = 30
progress_bar_y = 280
 
canvas = Canvas(box_2, width=progress_bar_width, height=progress_bar_height, bg="white", highlightthickness=0)
canvas.place(x=progress_bar_x, y=progress_bar_y)

progress_bar = canvas.create_rectangle(0, 0, 0, progress_bar_height, fill="#38B6FF")

def update_progress():
    global continue_scanning
    if continue_scanning:
        progress = 0
        while progress <= progress_bar_width:
            canvas.coords(progress_bar, (0, 0, progress, progress_bar_height))
            progress_label_text.set(f"Scanning... {int((progress / progress_bar_width) * 100)}%")
            scan.update()
            time.sleep(0.09)
            progress += 1
        complete_scan()
        continue_scanning = False

# Delay the execution of the update_progress() function
scan.after(100, update_progress)
scan.mainloop()
