from tkinter import *
from tkinter import messagebox, filedialog
import sqlite3
import datetime
import os
import shutil
import subprocess

def create_applicants_table():
    conn = sqlite3.connect('employeemanagement.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS applicants
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT NOT NULL,
                       position TEXT NOT NULL,
                       status TEXT NOT NULL,
                       application_date TEXT NOT NULL,
                       resume_path TEXT)''')
    conn.commit()
    conn.close()

def load_applicant_data(applicant_id=None):
    if applicant_id:
        conn = sqlite3.connect('employeemanagement.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM applicants WHERE id = ?", (applicant_id,))
        applicant = cursor.fetchone()
        conn.close()
        if applicant:
            Name_Entry.insert(0, applicant[1])
            Position_Entry.insert(0, applicant[2])
            Status_Entry.insert(0, applicant[3])
            Applicationdate_Entry.insert(0, applicant[4])
            Resume_Entry.insert(0, applicant[5])

def save_applicant():
    name = Name_Entry.get()
    position = Position_Entry.get()
    status = Status_Entry.get()
    application_date = Applicationdate_Entry.get()
    resume_path = Resume_Entry.get()

    if not all([name, position, status, application_date]):
        messagebox.showerror("Error", "All fields except Resume are required")
        return

    try:
        datetime.datetime.strptime(application_date, '%Y-%m-%d')
    except ValueError:
        messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD")
        return

    conn = sqlite3.connect('employeemanagement.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO applicants (name, position, status, application_date, resume_path)
                      VALUES (?, ?, ?, ?, ?)''',
                   (name, position, status, application_date, resume_path))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Applicant information saved successfully")
    clear_fields()

def clear_fields():
    Name_Entry.delete(0, END)
    Position_Entry.delete(0, END)
    Status_Entry.delete(0, END)
    Applicationdate_Entry.delete(0, END)
    Resume_Entry.delete(0, END)

def browse_resume():
    filename = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
    if filename:
        destination = os.path.join("resumes", os.path.basename(filename))
        os.makedirs("resumes", exist_ok=True)
        shutil.copy(filename, destination)
        Resume_Entry.delete(0, END)
        Resume_Entry.insert(0, destination)

def go_back():
    root.destroy()
    subprocess.Popen(["python", "tracking.py"])

# Create the applicants table if it doesn't exist
create_applicants_table()

root = Tk()
# root.state("zoomed")
root.title("Employee Management System - Applicant Details")
try:
    root.iconbitmap("z.ico")
except:
    pass  # If the icon file is not found, just skip it
root.config(bg="#1E2E56")

EMs = Label(text="Employee Management System", font=("Arial", 24, "bold"), bg="#1E2E56", fg="white")
EMs.place(x=610, y=13)

Applicantdetails = Label(text="Applicant Details", font=("Arial", 22, "bold"), bg="#1E2E56", fg="white")
Applicantdetails.place(x=620, y=70)

Name = Label(text="Name", bg="#1E2E56", fg="white", font=("Arial", 20))
Name.place(x=350, y=150)
Name_Entry = Entry(root, font=("Arial", 20))
Name_Entry.place(x=500, y=150)

Position = Label(text="Position", bg="#1E2E56", fg="white", font=("Arial", 20))
Position.place(x=340, y=240)
Position_Entry = Entry(root, font=("Arial", 20))
Position_Entry.place(x=500, y=240)

Status = Label(text="Status", bg="#1E2E56", fg="white", font=("Arial", 20))
Status.place(x=340, y=340)
Status_Entry = Entry(root, font=("Arial", 20))
Status_Entry.place(x=500, y=340)

Applicationdate = Label(text="Application Date", bg="#1E2E56", fg="white", font=("Arial", 20))
Applicationdate.place(x=280, y=440)
Applicationdate_Entry = Entry(root, font=("Arial", 20))
Applicationdate_Entry.place(x=500, y=440)
Applicationdate_Entry.insert(0, datetime.date.today().strftime("%Y-%m-%d"))

Resume = Label(text="Resume", bg="#1E2E56", fg="white", font=("Arial", 20))
Resume.place(x=320, y=550)
Resume_Entry = Entry(root, font=("Arial", 20))
Resume_Entry.place(x=500, y=550)
Browse_Button = Button(text="Browse", font=("Arial", 16), command=browse_resume)
Browse_Button.place(x=850, y=550)

Save_Button = Button(text="Save", font=("Arial", 20), command=save_applicant, bg="#4CAF50", fg="white")
Save_Button.place(x=1000, y=640)

Back = Button(text="Back", font=("Arial", 20), command=go_back, bg="#f44336", fg="white")
Back.place(x=1200, y=640)

# If you want to load existing applicant data, call this function with the applicant ID
# load_applicant_data(applicant_id)

mainloop()
