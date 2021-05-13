import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from DB_Functions import get_Vokabeln

HEIGHT = 300
WIDTH = 800


#Grundfenster
root = tk.Tk()
#Inhalt
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()
#hintergrund
canvas.configure(bg="#282721")


frame = tk.Frame(root, bg='#ed195a', bd=5)
frame.place(anchor='n', relx=0.5, rely=0.05, width=800, height=80 )


frame2 = tk.Frame(root, bg='#ed195a', bd=5)
frame2.place(anchor='n', relx=0.5, rely=0.33, width=800, height=80 )

#EntryWindow

entry = tk.Entry(frame, font=40)
entry.place(relx=0, rely=0.75, relwidth=0.7 , relheight=0.5, anchor='w')

entry2 = tk.Entry(frame2, font=40)
entry2.place(relx=0, rely=0.75, relwidth=0.7 , relheight=0.5, anchor='w')

var = tk.IntVar()


# button0 = tk.Button(frame, text="Traduction", font=40, command= lambda: button0_press(entry.get().lower().strip()))
# button0.place(relx=0.8,rely=0.5, relheight=1, relwidth=0.2, anchor="w")
# entry.focus_set()
# root.bind('<Return>', enter_klick)

# Infinitiv_Out = tk.StringVar()

# label = tk.Label(root, bd=5, textvariable=Infinitiv_Out)
# label.place(anchor='n', relx=0.5, rely=0.12, width=100, height=40 )

frame3 = tk.Frame(root, bg='#ed195a', bd=5)
frame3.place(relx=0.5, rely=0.97, relwidth=0.3, relheight=0.2, anchor='s')

button1 = tk.Button(frame2, text="Path auswählen", font=40, command= pathname)
button1.place(relx=1, rely=0.75, relwidth=0.3 , relheight=0.5, anchor='e')



button2 = tk.Button(frame3, text="Zusammengefügte Datei erstellen", font=40, command= zusammenfuhren)
button2.pack(side = "left", expand=True, fill="both")

# button3 = tk.Button(frame3, text="Definitionen \n Larousse \n Laden", font=40,command= button3_press)
# button3.pack(side = "left", expand=True, fill="both")

# button4 = tk.Button(frame3, text="Übersetzungen \n Leo \n laden", font=40,command= button4_press)
# button4.pack(side = "left", expand=True, fill="both")

# button5 = tk.Button(frame3, text="Nachgeschlagen \n Übersetzung \n laden", font=40,command= button5_press)
# button5.pack(side = "left", expand=True, fill="both")

root.mainloop()