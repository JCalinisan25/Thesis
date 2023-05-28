from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import os, time

# window
scan = Tk()
scan.title("Scanning Page")
scan.geometry("450x450")

# Flag to indicate whether to continue scanning or not
continue_scanning = True


def to_sign():
    global continue_scanning
    if messagebox.askyesno("Confirmation", "Are you sure you want to stop while scanning?"):
        continue_scanning = False
        scan.destroy()
        os.system('Dashboard.py')


def complete_scan():
    messagebox.showinfo("Successful", "Scan completed successfully!")


# Background
bg_0 = Image.open("img\\bg.jpg")
bck_pk = ImageTk.PhotoImage(bg_0.resize((450, 450)))

lbl = Label(scan, image=bck_pk, border=0)
lbl.place(x=1, y=1)

# profile
box_2 = Frame(scan, width=390, height=390, bg='#010F57')
box_2.place(x=30, y=30)

# quit
lg_btn = Button(box_2, bg="#010F57", bd=0, height=1, width=9, text="X", fg='white', font=('Arial', 15, 'bold'),
                cursor='hand2', command=to_sign)
lg_btn.place(x=310, y=1)

# To scan
progress_label = Label(box_2, text="Scanning...", font=('Arial', 15, 'bold'), fg='white', bg="#010F57")
progress_label.place(x=30, y=250)

progress_bar_width = 325
progress_bar_height = 10
progress_bar_x = 30
progress_bar_y = 280

canvas = Canvas(box_2, width=progress_bar_width, height=progress_bar_height, bg="white", highlightthickness=0)
canvas.place(x=progress_bar_x, y=progress_bar_y)

progress_bar = canvas.create_rectangle(0, 0, 0, progress_bar_height, fill="#38B6FF")


def animate_progress():
    global continue_scanning
    if continue_scanning:
        for i in range(progress_bar_width + 1):
            canvas.coords(progress_bar, (0, 0, i, progress_bar_height))
            scan.update()
            time.sleep(0.01)
            progress_label['text'] = 'Scanning... {}%'.format(int((i / progress_bar_width) * 100))
        complete_scan()


animate_progress()
scan.mainloop()