from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os

# window
result = Tk()
result.title("Detailed Results")
result.geometry("550x600")


def dash():
    result.destroy()
    os.system('Dashboard.py')


# Background
bg_0 = Image.open("img\\bg.jpg")
bck_pk = ImageTk.PhotoImage(bg_0.resize((550, 600)))

lbl = Label(result, image=bck_pk, border=0)
lbl.place(x=1, y=1)

# Header
box_1 = Frame(result, width=550, height=55, bg='#010F57')
box_1.place(x=3, y=5)
heading = Label(result, text='Detailed Report', fg='white', bg='#010F57', font=('Arial', 30, 'bold'))
heading.place(x=130, y=5)

# widget that manages a collection of windows/displays
notebook = ttk.Notebook(result)
notebook.pack(pady=70)

error = Image.open("img\\error.PNG")
ror_pk = ImageTk.PhotoImage(error.resize((100, 100)))

lbl = Label(notebook, image=ror_pk, border=0)
lbl.place(x=230, y=190)

# Tab results
gback = Button(notebook)
dos = Frame(notebook)
em_c = Frame(notebook)
logo = Frame(notebook)
url = Frame(notebook)
hist = Frame(notebook)
chart = Frame(notebook)

notebook.add(dos, text="Domain of Sender\t          ")
notebook.add(em_c, text="Email Content\t     ")
notebook.add(logo, text="Logo\t    ")
notebook.add(url, text="URL/s\t    ")
notebook.add(hist, text="History\t    ")
notebook.add(chart, text="Chart\t    ")

#Domain Tab
dos.configure(background='#010F57')
Label(dos, text="The domain '@d1scord.com' has been found to be fraudulent. "
                "\nIt appears to be mimicking 'discord.com'.", fg='white', width=75, height=50,
      bg='#010F57', bd=0, font=('Arial', 9, 'bold')).pack()

#Email Tab
em_c.configure(background='#010F57')
Label(em_c, text="The email content has been found to be fraudulent.", fg='white', width=75, height=50,
      bg='#010F57', bd=0, font=('Arial', 9, 'bold')).pack()

#Logo Tab
logo.configure(background='#010F57')
Label(logo, text="The logo has been found to be fraudulent.", fg='white', width=75, height=50,
      bg='#010F57', bd=0, font=('Arial', 9, 'bold')).pack()

#URL Tab
url.configure(background='#010F57')
Label(url, text="The URL has been found a phishing site.", fg='white', width=75, height=50,
      bg='#010F57', bd=0, font=('Arial', 9, 'bold')).pack()

#History Tab
hist.configure(background='#010F57')
bg = ttk.Style
table = ttk.Treeview(hist, columns =("Date", "Name", "Source", "Response"), show="headings")
table.pack()
table.heading("Date", text="Date")
table.heading("Name", text="Name")
table.heading("Source", text="Source")
table.heading("Response", text="Response")
table.insert(parent="", index=0, iid=0, text="Row 1", values=("03/15/2023", "Click Now!", "Phishing","Blocked"))
table.insert(parent="", index=1, iid=1, text="Row 2", values=("03/18/2023", "Click to Win!", "Phishing","Blocked"))
table.column("Date", width=100)
table.column("Name", width=200)
table.column("Source", width=100)
table.column("Response", width=100)
table.place(x=10,y=10)

#Chart Tab
chart.configure(background='#010F57')
empty_frame = ttk.Frame(chart, height=100)
fig = Figure(figsize=(4.9, 4), dpi=100)
ax = fig.add_subplot(111)
data = {"Phishing": 2, "Legitimate": 10}
ax.pie(data.values(), labels=data.keys(), shadow=True, explode=(0.1, 0.1), autopct='%1.1f%%', startangle=90)
ax.set_title("Phishing Emails")
canvas = FigureCanvasTkAgg(fig, master=chart)
canvas.draw()
canvas.get_tk_widget().pack(pady=10)

#Exit Button
Button(notebook, text="X", fg='white', width=1, height=0, bg='#010F57', font=('Arial', 10, 'bold'), bd=0,
       command=dash).place(x=515, y=27)
result.mainloop()
