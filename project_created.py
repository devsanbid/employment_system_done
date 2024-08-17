from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import subprocess
from tkcalendar import DateEntry
from datetime import datetime

def save_project():
    name = name_entry.get()
    status = status_var.get()
    start_date = start_date_entry.get_date().strftime('%Y/%m/%d')
    end_date = end_date_entry.get_date().strftime('%Y/%m/%d')

    if not name:
        messagebox.showerror("Error", "Project name is required")
        return

    conn = sqlite3.connect('employeemanagement.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO projects (name, status, start_date, end_date)
                      VALUES (?, ?, ?, ?)''', (name, status, start_date, end_date))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Project added successfully")
    root.destroy()
    subprocess.Popen(["python", "projects.py"])

def cancel():
    root.destroy()
    subprocess.Popen(["python", "projects.py"])

root = Tk()
root.title("Employee Management System - Add Project")
root.config(bg="#1E2E56")
# root.state('zoomed')  # This will maximize the window

title_label = Label(root, text="Add New Project", font=("Arial", 36, "bold"), bg="#1E2E56", fg="white")
title_label.pack(pady=40)

# Create a main frame to hold all the widgets
main_frame = Frame(root, bg="#1E2E56")
main_frame.pack(expand=True)

# Project Name
name_label = Label(main_frame, text="Project Name:", font=("Arial", 24), bg="#1E2E56", fg="white")
name_label.grid(row=0, column=0, pady=20, sticky='w')
name_entry = Entry(main_frame, font=("Arial", 24), width=40)
name_entry.grid(row=0, column=1, pady=20, padx=20)

# Status
status_label = Label(main_frame, text="Status:", font=("Arial", 24), bg="#1E2E56", fg="white")
status_label.grid(row=1, column=0, pady=20, sticky='w')
status_var = StringVar(value="Active")
status_options = ["Active", "Completed", "On Hold"]
status_menu = ttk.Combobox(main_frame, textvariable=status_var, values=status_options, font=("Arial", 24), width=38)
status_menu.grid(row=1, column=1, pady=20, padx=20)

# Start Date
start_date_label = Label(main_frame, text="Start Date:", font=("Arial", 24), bg="#1E2E56", fg="white")
start_date_label.grid(row=2, column=0, pady=20, sticky='w')
start_date_entry = DateEntry(main_frame, width=38, background='darkblue', foreground='white', borderwidth=2, font=("Arial", 24))
start_date_entry.grid(row=2, column=1, pady=20, padx=20)

# End Date
end_date_label = Label(main_frame, text="End Date:", font=("Arial", 24), bg="#1E2E56", fg="white")
end_date_label.grid(row=3, column=0, pady=20, sticky='w')
end_date_entry = DateEntry(main_frame, width=38, background='darkblue', foreground='white', borderwidth=2, font=("Arial", 24))
end_date_entry.grid(row=3, column=1, pady=20, padx=20)

# Buttons
button_frame = Frame(main_frame, bg="#1E2E56")
button_frame.grid(row=4, column=0, columnspan=2, pady=40)

save_button = Button(button_frame, text="Save", command=save_project, font=("Arial", 24), bg="#4CAF50", fg="white", padx=40, pady=20)
save_button.pack(side=LEFT, padx=20)

cancel_button = Button(button_frame, text="Cancel", command=cancel, font=("Arial", 24), bg="#f44336", fg="white", padx=40, pady=20)
cancel_button.pack(side=LEFT, padx=20)

# Configure style for Combobox
style = ttk.Style()
style.theme_use('clam')
style.configure('TCombobox', fieldbackground='white', background='white', foreground='black')

root.mainloop()
