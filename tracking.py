from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import subprocess

def load_applicants():
    conn = sqlite3.connect('employeemanagement.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, position, status, department FROM applicants ORDER BY department DESC")
    applicants = cursor.fetchall()
    conn.close()
    return applicants

def display_applicants():
    applicants = load_applicants()
    for i in tree.get_children():
        tree.delete(i)
    for applicant in applicants:
        tree.insert('', 'end', values=applicant)

def add_new_applicant():
    root.destroy()
    subprocess.Popen(["python", "applicantdetails.py"])

def search_applicants():
    name = Applicant_Entry.get().lower()
    position = Position_Entry.get().lower()
    status = Status_Entry.get().lower()
    department = Department_Entry.get().lower()

    conn = sqlite3.connect('employeemanagement.db')
    cursor = conn.cursor()
    
    query = """SELECT id, name, position, status, department 
               FROM applicants 
               WHERE LOWER(name) LIKE ? AND LOWER(position) LIKE ? AND LOWER(status) LIKE ? AND LOWER(department) LIKE ?
               ORDER BY department DESC"""
    cursor.execute(query, (f'%{name}%', f'%{position}%', f'%{status}%', f'%{department}%'))
    
    applicants = cursor.fetchall()
    conn.close()

    for i in tree.get_children():
        tree.delete(i)
    for applicant in applicants:
        tree.insert('', 'end', values=applicant)

def view_details():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select an applicant to view details.")
        return
    applicant_id = tree.item(selected_item)['values'][0]
    root.destroy()
    subprocess.Popen(["python", "applicantdetails.py", str(applicant_id)])

def go_back():
    root.destroy()
    subprocess.Popen(["python", "dashboard.py"])

root = Tk()
root.title("Employee Management System - Applicant Tracking")
root.config(bg="#1E2E56")
root.geometry("1600x900")  # Adjusted for more space

EMs = Label(text="Employee Management System", font=("Arial", 24, "bold"), bg="#1E2E56", fg="white")
EMs.place(x=610, y=13)

Applicant = Label(text="Applicant Name", bg="#1E2E56", fg="white", font=("Arial", 20))
Applicant.place(x=50, y=100)
Applicant_Entry = Entry(root, font=("Arial", 20))
Applicant_Entry.place(x=250, y=100)

Position = Label(text="Position", bg="#1E2E56", fg="white", font=("Arial", 20))
Position.place(x=550, y=100)
Position_Entry = Entry(root, font=("Arial", 20))
Position_Entry.place(x=700, y=100)

Status = Label(text="Status", bg="#1E2E56", fg="white", font=("Arial", 20))
Status.place(x=1000, y=100)
Status_Entry = Entry(root, font=("Arial", 20))
Status_Entry.place(x=1100, y=100)

Department = Label(text="Department", bg="#1E2E56", fg="white", font=("Arial", 20))
Department.place(x=50, y=150)
Department_Entry = Entry(root, font=("Arial", 20))
Department_Entry.place(x=250, y=150)

Search_Button = Button(text="Search", font=("Arial", 16), command=search_applicants, bg="#4CAF50", fg="white")
Search_Button.place(x=1400, y=150)

# Create Treeview
tree = ttk.Treeview(root, columns=('ID', 'Name', 'Position', 'Status', 'Department'), show='headings')
tree.heading('ID', text='ID')
tree.heading('Name', text='Applicant Name')
tree.heading('Position', text='Position')
tree.heading('Status', text='Status')
tree.heading('Department', text='Department')
tree.column('ID', width=50)
tree.column('Name', width=300)
tree.column('Position', width=200)
tree.column('Status', width=150)
tree.column('Department', width=150)
tree.place(x=50, y=200, width=1500, height=400)

button_frame = Frame(root, bg="#1E2E56")
button_frame.place(x=50, y=650)

Add_Applicant = Button(button_frame, text="Add Applicant", font=("Arial", 20), command=add_new_applicant, bg="#4CAF50", fg="white")
Add_Applicant.pack(side=LEFT, padx=10)

Viewdetails = Button(text="View details", font=("Arial", 20), command=view_details, bg="#2196F3", fg="white")
Viewdetails.place(x=1000, y=650)

Back = Button(text="Back", font=("Arial", 20), command=go_back, bg="#f44336", fg="white")
Back.place(x=1300, y=650)

# Load initial applicants
display_applicants()

mainloop()
