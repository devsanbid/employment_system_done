from tkinter import *
from tkinter import messagebox, filedialog
import sqlite3
import os
import shutil
import subprocess
import sys  # Import sys to access command line arguments

def create_applicants_table():
    conn = sqlite3.connect('employeemanagement.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS applicants
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT NOT NULL,
                       position TEXT NOT NULL,
                       department TEXT NOT NULL,
                       status TEXT NOT NULL,
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
            Department_Entry.insert(0, applicant[3])
            Status_Entry.insert(0, applicant[4])
            Resume_Entry.insert(0, applicant[5])

def save_applicant():
    name = Name_Entry.get()
    position = Position_Entry.get()
    department = Department_Entry.get()
    status = Status_Entry.get()
    resume_path = Resume_Entry.get()

    if not all([name, position, department, status]):
        messagebox.showerror("Error", "All fields except Resume are required")
        return

    conn = sqlite3.connect('employeemanagement.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO applicants (name, position, department, status, resume_path)
                      VALUES (?, ?, ?, ?, ?)''',
                   (name, position, department, status, resume_path))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Applicant information saved successfully")
    clear_fields()

def clear_fields():
    Name_Entry.delete(0, END)
    Position_Entry.delete(0, END)
    Department_Entry.delete(0, END)
    Status_Entry.delete(0, END)
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
Position.place(x=340, y=220)
Position_Entry = Entry(root, font=("Arial", 20))
Position_Entry.place(x=500, y=220)

Department = Label(text="Department", bg="#1E2E56", fg="white", font=("Arial", 20))
Department.place(x=320, y=290)
Department_Entry = Entry(root, font=("Arial", 20))
Department_Entry.place(x=500, y=290)

Status = Label(text="Status", bg="#1E2E56", fg="white", font=("Arial", 20))
Status.place(x=340, y=360)
Status_Entry = Entry(root, font=("Arial", 20))
Status_Entry.place(x=500, y=360)

Resume = Label(text="Resume", bg="#1E2E56", fg="white", font=("Arial", 20))
Resume.place(x=320, y=430)
Resume_Entry = Entry(root, font=("Arial", 20))
Resume_Entry.place(x=500, y=430)
Browse_Button = Button(text="Browse", font=("Arial", 16), command=browse_resume)
Browse_Button.place(x=850, y=430)

Save_Button = Button(text="Save", font=("Arial", 20), command=save_applicant, bg="#4CAF50", fg="white")
Save_Button.place(x=500, y=500)

Back = Button(text="Back", font=("Arial", 20), command=go_back, bg="#f44336", fg="white")
Back.place(x=700, y=500)

# Load applicant data if an ID is provided
if len(sys.argv) > 1:
    applicant_id = sys.argv[1]
    load_applicant_data(applicant_id)

mainloop()
