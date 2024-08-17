from tkinter import *
from tkinter import ttk
import sqlite3
import subprocess

def fetch_projects():
    conn = sqlite3.connect('employeemanagement.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, status, start_date, end_date FROM projects")
    projects = cursor.fetchall()
    conn.close()
    return projects

def populate_table(projects):
    for i in tree.get_children():
        tree.delete(i)
    for project in projects:
        tree.insert('', 'end', values=project)

def mark_complete():
    selected_item = tree.selection()
    if not selected_item:
        return
    project_name = tree.item(selected_item)['values'][0]
    conn = sqlite3.connect('employeemanagement.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE projects SET status = 'Completed' WHERE name = ?", (project_name,))
    conn.commit()
    conn.close()
    populate_table(fetch_projects())

def add_new_project():
    root.destroy()
    subprocess.Popen(["python", "project_created.py"])

def exit_page():
    root.destroy()
    subprocess.Popen(["python", "dashboard.py"])

root = Tk()
root.title("Employee Management System - Projects")
root.config(bg="#1E2E56")
root.geometry("1600x900")
# root.state('zoomed')  # This will maximize the window

# Title and header image
title_frame = Frame(root, bg="#1E2E56")
title_frame.pack(fill=X)

title_label = Label(title_frame, text="Employee Management System", font=("Arial", 24, "bold"), bg="#1E2E56", fg="white")
title_label.pack(pady=10)

# You can replace this with an actual image
header_image = Label(title_frame, bg="lightgray", height=3)
header_image.pack(fill=X)

# Projects label
projects_label = Label(root, text="Projects", font=("Arial", 20, "bold"), bg="#1E2E56", fg="white")
projects_label.pack(pady=20)

# Table
table_frame = Frame(root, bg="#1E2E56")
table_frame.pack(pady=20, padx=50, fill=BOTH, expand=TRUE)

tree = ttk.Treeview(table_frame, columns=('Name', 'Status', 'Start date', 'End date'), show='headings', height=15)
tree.heading('Name', text='Name')
tree.heading('Status', text='Status')
tree.heading('Start date', text='Start date')
tree.heading('End date', text='End date')

tree.column('Name', width=300, anchor=CENTER)
tree.column('Status', width=200, anchor=CENTER)
tree.column('Start date', width=200, anchor=CENTER)
tree.column('End date', width=200, anchor=CENTER)

tree.pack(fill=BOTH, expand=TRUE)

# Configure colors and fonts
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", 
                background="#1E2E56", 
                foreground="white", 
                fieldbackground="#1E2E56",
                borderwidth=0,
                font=('Arial', 14))
style.configure("Treeview.Heading", font=('Arial', 16, 'bold'), foreground="white", background="#0A7E8C")
style.map('Treeview', background=[('selected', '#0A7E8C')])

# Buttons
button_frame = Frame(root, bg="#1E2E56")
button_frame.pack(pady=30)

add_project_button = Button(button_frame, text="Add Project", font=("Arial", 16), command=add_new_project, bg="#4CAF50", fg="white", padx=20, pady=10)
add_project_button.pack(side=LEFT, padx=20)

mark_complete_button = Button(button_frame, text="Mark complete", font=("Arial", 16), command=mark_complete, bg="#2196F3", fg="white", padx=20, pady=10)
mark_complete_button.pack(side=LEFT, padx=20)

exit_button = Button(button_frame, text="Exit", font=("Arial", 16), command=exit_page, bg="#f44336", fg="white", padx=20, pady=10)
exit_button.pack(side=LEFT, padx=20)

# Populate table
projects = fetch_projects()
populate_table(projects)

root.mainloop()
