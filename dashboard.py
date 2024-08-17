from tkinter import *
from tkinter import messagebox
import sqlite3
import subprocess

def create_tables():
    conn = sqlite3.connect('employeemanagement.db')
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS projects
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT NOT NULL,
                       description TEXT,
                       start_date TEXT,
                       end_date TEXT,
                       status TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS employees
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT NOT NULL,
                       position TEXT,
                       department TEXT,
                       email TEXT,
                       phone TEXT,
                       address TEXT,
                       resume_path TEXT
                       )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS events
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT NOT NULL,
                       date TEXT NOT NULL,
                       participants TEXT NOT NULL,
                       location TEXT NOT NULL)''')
 
    cursor.execute('''CREATE TABLE IF NOT EXISTS applicants
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT NOT NULL,
                       position TEXT,
                       status TEXT,
                       department TEXT,
                       resume_path TEXT)''')
    
    conn.commit()
    conn.close()

def get_counts():
    conn = sqlite3.connect('employeemanagement.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM projects")
    project_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM employees")
    employee_count = cursor.fetchone()[0]
    
    conn.close()
    return project_count, employee_count

def open_user_profile():
    root.destroy()
    subprocess.Popen(["python", "userprofile.py", str(current_user_id)])

def open_projects():
    root.destroy()
    subprocess.Popen(["python", "projects.py"])

def open_employees():
    root.destroy()
    subprocess.Popen(["python", "employeedetails.py"])

def open_applicant_tracking():
    root.destroy()
    subprocess.Popen(["python", "tracking.py"])

def open_event():
    root.destroy()
    subprocess.Popen(["python", "event.py"])

def logout():
    root.destroy()
    subprocess.Popen(["python", "a_login.py"])

# Create necessary tables
create_tables()

# Assume we get the username and user ID from the login process
current_user = "Steve Roy"  # This should be passed from the login page
current_user_id = 1

root = Tk()
root.title("Employee Management System - Dashboard")
root.config(bg="#1E2E56")
root.geometry("1400x800")  # Adjusted for more space

try:
    root.iconbitmap("z.ico")
except:
    pass  # If the icon file is not found, just skip it

project_count, employee_count = get_counts()

EMs = Label(text="Employee Management System", font=("Arial", 24, "bold"), bg="#1E2E56", fg="white")
EMs.place(x=500, y=10)

Photo = Label(text="  Photo  ", font=("Arial", 20), bg="#FFFFFF", fg="black", height=2, width=8)
Photo.place(x=140, y=75)

Steveroy = Label(text=current_user, bg="#1E2E56", fg="#0AAFA5", font=("Arial", 20))
Steveroy.place(x=130, y=150)

Userprofile = Button(text="User Profile", bg="#0AAFA5", fg="white", font=("Arial", 16), command=open_user_profile)
Userprofile.place(x=1200, y=100)

Projects = Button(text=f"Projects ({project_count})", bg="#1E2E56", fg="white", font=("Arial", 20), command=open_projects)
Projects.place(x=200, y=210)

Employees = Button(text=f"Employees ({employee_count})", bg="#1E2E56", fg="white", font=("Arial", 20), command=open_employees)
Employees.place(x=200, y=290)

Applicanttracking = Button(text="Applicant Tracking", bg="#1E2E56", fg="white", font=("Arial", 20), command=open_applicant_tracking)
Applicanttracking.place(x=190, y=370)

Event = Button(text="Event", bg="#1E2E56", fg="white", font=("Arial", 20), command=open_event)
Event.place(x=210, y=450)

Logout = Button(text="Logout", font=("Arial", 20), command=logout, bg="#f44336", fg="white")
Logout.place(x=220, y=600)

Exit = Button(text="Exit", font=("Arial", 20), command=root.quit, bg="#555555", fg="white")
Exit.place(x=950, y=600)

mainloop()
