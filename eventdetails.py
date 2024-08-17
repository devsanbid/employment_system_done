from tkinter import *
from tkinter import messagebox
import sqlite3
import datetime
import subprocess

def create_events_table():
    conn = sqlite3.connect('employeemanagement.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS events
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT NOT NULL,
                       date TEXT NOT NULL,
                       participants TEXT NOT NULL,
                       location TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def load_event_data(event_id=None):
    if event_id:
        conn = sqlite3.connect('employeemanagement.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
        event = cursor.fetchone()
        conn.close()
        if event:
            Name_Entry.insert(0, event[1])
            Date_Entry.insert(0, event[2])
            Participants_Entry.insert(0, event[3])
            Location_Entry.insert(0, event[4])

def save_event():
    name = Name_Entry.get()
    date = Date_Entry.get()
    participants = Participants_Entry.get()
    location = Location_Entry.get()

    if not all([name, date, participants, location]):
        messagebox.showerror("Error", "All fields are required")
        return

    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD")
        return

    conn = sqlite3.connect('employeemanagement.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO events (name, date, participants, location)
                      VALUES (?, ?, ?, ?)''',
                   (name, date, participants, location))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Event information saved successfully")
    clear_fields()

def clear_fields():
    Name_Entry.delete(0, END)
    Date_Entry.delete(0, END)
    Participants_Entry.delete(0, END)
    Location_Entry.delete(0, END)

def go_back():
    root.destroy()
    subprocess.Popen(["python", "event.py"])

# Create the events table if it doesn't exist
create_events_table()

root = Tk()
root.title("Employee Management System - Event Details")
root.config(bg="#1E2E56")
root.geometry("1600x900")  # Adjusted for more space

EMs = Label(text="Employee Management System", font=("Arial", 24, "bold"), bg="#1E2E56", fg="white")
EMs.place(x=610, y=13)

Eventdetails = Label(text="Event Details", font=("Arial", 22, "bold"), bg="#1E2E56", fg="white")
Eventdetails.place(x=700, y=90)

Name = Label(text="Name", bg="#1E2E56", fg="white", font=("Arial", 20))
Name.place(x=250, y=190)
Name_Entry = Entry(root, font=("Arial", 20))
Name_Entry.place(x=480, y=190)

Date = Label(text="Date", bg="#1E2E56", fg="white", font=("Arial", 20))
Date.place(x=250, y=290)
Date_Entry = Entry(root, font=("Arial", 20))
Date_Entry.place(x=480, y=290)
Date_Entry.insert(0, datetime.date.today().strftime("%Y-%m-%d"))

Participants = Label(text="Participants", bg="#1E2E56", fg="white", font=("Arial", 20))
Participants.place(x=220, y=390)
Participants_Entry = Entry(root, font=("Arial", 20))
Participants_Entry.place(x=480, y=390)

Location = Label(text="Location", bg="#1E2E56", fg="white", font=("Arial", 20))
Location.place(x=230, y=490)
Location_Entry = Entry(root, font=("Arial", 20))
Location_Entry.place(x=480, y=490)

Save_Button = Button(text="Save", font=("Arial", 20), command=save_event, bg="#4CAF50", fg="white")
Save_Button.place(x=1000, y=640)

Back = Button(text="Back", font=("Arial", 20), command=go_back, bg="#f44336", fg="white")
Back.place(x=1200, y=640)

# If you want to load existing event data, call this function with the event ID
# load_event_data(event_id)

mainloop()
