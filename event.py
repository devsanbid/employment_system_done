from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import subprocess
import datetime

def load_events():
    conn = sqlite3.connect('employeemanagement.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, date, location FROM events ORDER BY date")
    events = cursor.fetchall()
    conn.close()
    return events

def display_events():
    events = load_events()
    for i in tree.get_children():
        tree.delete(i)
    for event in events:
        tree.insert('', 'end', values=event)

def add_event():
    root.destroy()
    subprocess.Popen(["python", "eventdetails.py"])

def search_events():
    search_term = Event_Entry.get().lower()
    date = Date_Entry.get()
    location = Location_Entry.get().lower()

    conn = sqlite3.connect('employeemanagement.db')
    cursor = conn.cursor()
    
    query = "SELECT id, name, date, location FROM events WHERE LOWER(name) LIKE ? AND date LIKE ? AND LOWER(location) LIKE ? ORDER BY date"
    cursor.execute(query, (f'%{search_term}%', f'%{date}%', f'%{location}%'))
    
    events = cursor.fetchall()
    conn.close()

    for i in tree.get_children():
        tree.delete(i)
    for event in events:
        tree.insert('', 'end', values=event)

def view_details():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select an event to view details.")
        return
    event_id = tree.item(selected_item)['values'][0]
    root.destroy()
    subprocess.Popen(["python", "eventdetails.py", str(event_id)])

def go_back():
    root.destroy()
    subprocess.Popen(["python", "dashboard.py"])

root = Tk()
root.title("Employee Management System - Events")
root.config(bg="#1E2E56")
root.geometry("1600x900")  # Adjusted for more space

EMs = Label(text="Employee Management System", font=("Arial", 24, "bold"), bg="#1E2E56", fg="white")
EMs.place(x=610, y=13)

Event = Label(text="Event Name", bg="#1E2E56", fg="white", font=("Arial", 20))
Event.place(x=50, y=100)
Event_Entry = Entry(root, font=("Arial", 20))
Event_Entry.place(x=200, y=100)

Date = Label(text="Date", bg="#1E2E56", fg="white", font=("Arial", 20))
Date.place(x=550, y=100)
Date_Entry = Entry(root, font=("Arial", 20))
Date_Entry.place(x=650, y=100)
Date_Entry.insert(0, datetime.date.today().strftime("%Y-%m-%d"))

Location = Label(text="Location", bg="#1E2E56", fg="white", font=("Arial", 20))
Location.place(x=1000, y=100)
Location_Entry = Entry(root, font=("Arial", 20))
Location_Entry.place(x=1150, y=100)

Search_Button = Button(text="Search", font=("Arial", 16), command=search_events, bg="#4CAF50", fg="white")
Search_Button.place(x=1400, y=100)

# Create Treeview
tree = ttk.Treeview(root, columns=('ID', 'Name', 'Date', 'Location'), show='headings')
tree.heading('ID', text='ID')
tree.heading('Name', text='Event Name')
tree.heading('Date', text='Date')
tree.heading('Location', text='Location')
tree.column('ID', width=50)
tree.column('Name', width=300)
tree.column('Date', width=100)
tree.column('Location', width=200)
tree.place(x=50, y=200, width=1500, height=400)

button_frame = Frame(root, bg="#1E2E56")
button_frame.place(x=50, y=650)

Add_Event = Button(button_frame, text="Add Event", font=("Arial", 20), command=add_event, bg="#4CAF50", fg="white")
Add_Event.pack(side=LEFT, padx=10)

Viewdetails = Button(text="View details", font=("Arial", 20), command=view_details, bg="#2196F3", fg="white")
Viewdetails.place(x=1000, y=650)

Back = Button(text="Back", font=("Arial", 20), command=go_back, bg="#f44336", fg="white")
Back.place(x=1300, y=650)

# Load initial events
display_events()

mainloop()
