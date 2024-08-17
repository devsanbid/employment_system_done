from tkinter import *
from tkinter import ttk
import sqlite3
import subprocess

def fetch_employees():
    conn = sqlite3.connect('employeemanagement.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, department, position, 'Active' as status FROM employees")
    employees = cursor.fetchall()
    conn.close()
    return employees

def populate_table(employees):
    for i in tree.get_children():
        tree.delete(i)
    for employee in employees:
        tree.insert('', 'end', values=employee)

def search_employees():
    search_term = search_entry.get().lower()
    all_employees = fetch_employees()
    filtered_employees = [emp for emp in all_employees if search_term in emp[0].lower()]
    populate_table(filtered_employees)

def add_new_employee():
    root.destroy()
    subprocess.Popen(["python", "employees.py"])

def exit_page():
    root.destroy()
    subprocess.Popen(["python", "dashboard.py"])

root = Tk()
root.title("Employee Management System - Employees")
root.config(bg="#1E2E56")
# root.state('zoomed')  # This will maximize the window

# Title
title_label = Label(root, text="Employee Management System", font=("Arial", 36, "bold"), bg="#1E2E56", fg="white")
title_label.pack(pady=30)

# Search bar
search_frame = Frame(root, bg="#1E2E56")
search_frame.pack(pady=30)

search_entry = Entry(search_frame, font=("Arial", 24), width=40)
search_entry.pack(side=LEFT, padx=20)

search_button = Button(search_frame, text="Search", font=("Arial", 20), command=search_employees, bg="#4CAF50", fg="white", padx=20, pady=10)
search_button.pack(side=LEFT)

# Table
table_frame = Frame(root, bg="#1E2E56")
table_frame.pack(pady=30, padx=50, fill=BOTH, expand=TRUE)

tree = ttk.Treeview(table_frame, columns=('Name', 'Department', 'Position', 'Status'), show='headings', height=15)
tree.heading('Name', text='Name')
tree.heading('Department', text='Department')
tree.heading('Position', text='Position')
tree.heading('Status', text='Status')

tree.column('Name', width=400, anchor=CENTER)
tree.column('Department', width=300, anchor=CENTER)
tree.column('Position', width=300, anchor=CENTER)
tree.column('Status', width=200, anchor=CENTER)

tree.pack(fill=BOTH, expand=TRUE)

# Configure colors and fonts
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", 
                background="#1E2E56", 
                foreground="white", 
                fieldbackground="#1E2E56",
                borderwidth=0,
                font=('Arial', 16))
style.configure("Treeview.Heading", font=('Arial', 18, 'bold'), foreground="white", background="#0A7E8C")
style.map('Treeview', background=[('selected', '#0A7E8C')])

# Buttons
button_frame = Frame(root, bg="#1E2E56")
button_frame.pack(pady=30)

add_button = Button(button_frame, text="Add new employee", font=("Arial", 20), command=add_new_employee, bg="#2196F3", fg="white", padx=20, pady=10)
add_button.pack(side=LEFT, padx=20)

exit_button = Button(button_frame, text="Exit", font=("Arial", 20), command=exit_page, bg="#f44336", fg="white", padx=20, pady=10)
exit_button.pack(side=LEFT, padx=20)

# Populate table
employees = fetch_employees()
populate_table(employees)

root.mainloop()

