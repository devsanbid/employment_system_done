from tkinter import *
from tkinter import messagebox, filedialog
import sqlite3
import os
import shutil
import subprocess

def create_employees_table():
    conn = sqlite3.connect('employeemanagement.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS employees
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT NOT NULL,
                       position TEXT,
                       department TEXT,
                       email TEXT,
                       phone TEXT,
                       address TEXT,
                       resume_path TEXT)''')
    conn.commit()
    conn.close()

def load_employee_data(employee_id=None):
    if employee_id:
        conn = sqlite3.connect('employeemanagement.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
        employee = cursor.fetchone()
        conn.close()
        if employee:
            Name_Entry.insert(0, employee[1])
            Position_Entry.insert(0, employee[2])
            Department_Entry.insert(0, employee[3])
            Email_Entry.insert(0, employee[4])
            Phone_Entry.insert(0, employee[5])
            Address_Entry.insert(0, employee[6])
            Resume_Entry.insert(0, employee[7])

def save_employee():
    name = Name_Entry.get()
    position = Position_Entry.get()
    department = Department_Entry.get()
    email = Email_Entry.get()
    phone = Phone_Entry.get()
    address = Address_Entry.get()
    resume_path = Resume_Entry.get()

    if not name:
        messagebox.showerror("Error", "Name is required")
        return

    conn = sqlite3.connect('employeemanagement.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO employees (name, position, department, email, phone, address, resume_path)
                      VALUES (?, ?, ?, ?, ?, ?, ?)''',
                   (name, position, department, email, phone, address, resume_path))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Employee information saved successfully")
    clear_fields()

def clear_fields():
    Name_Entry.delete(0, END)
    Position_Entry.delete(0, END)
    Department_Entry.delete(0, END)
    Email_Entry.delete(0, END)
    Phone_Entry.delete(0, END)
    Address_Entry.delete(0, END)
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
    subprocess.Popen(["python", "employeedetails.py"])

# Create the employees table if it doesn't exist
create_employees_table()

root = Tk()
root.title("Employee Management System - Employee Details")
#root.state('zoomed')  # Maximize the window
try:
    root.iconbitmap("z.ico")
except:
    pass  # If the icon file is not found, just skip it
root.config(bg="#1E2E56")

EMs = Label(text="Employee Management System", font=("Arial", 24, "bold"), bg="#1E2E56", fg="white")
EMs.pack(pady=20)

EmployeeDetails = Label(text="Employee Details", font=("Arial", 22, "bold"), bg="#1E2E56", fg="white")
EmployeeDetails.pack(pady=10)

frame = Frame(root, bg="#1E2E56")
frame.pack(expand=True)

Name = Label(frame, text="Name", bg="#1E2E56", fg="white", font=("Arial", 20))
Name.grid(row=0, column=0, sticky="e", padx=10, pady=10)
Name_Entry = Entry(frame, font=("Arial", 20), width=30)
Name_Entry.grid(row=0, column=1, padx=10, pady=10)

Position = Label(frame, text="Position", bg="#1E2E56", fg="white", font=("Arial", 20))
Position.grid(row=1, column=0, sticky="e", padx=10, pady=10)
Position_Entry = Entry(frame, font=("Arial", 20), width=30)
Position_Entry.grid(row=1, column=1, padx=10, pady=10)

Department = Label(frame, text="Department", bg="#1E2E56", fg="white", font=("Arial", 20))
Department.grid(row=2, column=0, sticky="e", padx=10, pady=10)
Department_Entry = Entry(frame, font=("Arial", 20), width=30)
Department_Entry.grid(row=2, column=1, padx=10, pady=10)

Email = Label(frame, text="Email", bg="#1E2E56", fg="white", font=("Arial", 20))
Email.grid(row=3, column=0, sticky="e", padx=10, pady=10)
Email_Entry = Entry(frame, font=("Arial", 20), width=30)
Email_Entry.grid(row=3, column=1, padx=10, pady=10)

Phone = Label(frame, text="Phone", bg="#1E2E56", fg="white", font=("Arial", 20))
Phone.grid(row=4, column=0, sticky="e", padx=10, pady=10)
Phone_Entry = Entry(frame, font=("Arial", 20), width=30)
Phone_Entry.grid(row=4, column=1, padx=10, pady=10)

Address = Label(frame, text="Address", bg="#1E2E56", fg="white", font=("Arial", 20))
Address.grid(row=5, column=0, sticky="e", padx=10, pady=10)
Address_Entry = Entry(frame, font=("Arial", 20), width=30)
Address_Entry.grid(row=5, column=1, padx=10, pady=10)

Resume = Label(frame, text="Resume", bg="#1E2E56", fg="white", font=("Arial", 20))
Resume.grid(row=6, column=0, sticky="e", padx=10, pady=10)
Resume_Entry = Entry(frame, font=("Arial", 20), width=30)
Resume_Entry.grid(row=6, column=1, padx=10, pady=10)
Browse_Button = Button(frame, text="Browse", font=("Arial", 16), command=browse_resume)
Browse_Button.grid(row=6, column=2, padx=10, pady=10)

button_frame = Frame(frame, bg="#1E2E56")
button_frame.grid(row=7, column=0, columnspan=3, pady=20)

Save_Button = Button(button_frame, text="Save", font=("Arial", 20), command=save_employee, bg="#4CAF50", fg="white")
Save_Button.pack(side=LEFT, padx=10)

Back = Button(button_frame, text="Back", font=("Arial", 20), command=go_back, bg="#f44336", fg="white")
Back.pack(side=LEFT, padx=10)

# If you want to load existing employee data, call this function with the employee ID
# load_employee_data(employee_id)

mainloop()
