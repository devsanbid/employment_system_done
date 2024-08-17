from tkinter import *
from tkinter import messagebox
import sqlite3
import subprocess
import re

def load_user_data(user_id):
    conn = sqlite3.connect('employeemanagement.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def save_user_data():
    name = Name_Entry.get()
    email = Email_Entry.get()
    phone = Phone_Entry.get()
    position = Position_Entry.get()
    department = Department_Entry.get()
    address = Address_Entry.get()

    if not all([name, email, phone, position, department, address]):
        messagebox.showerror("Error", "All fields are required")
        return

    if not validate_email(email):
        messagebox.showerror("Error", "Invalid email format")
        return

    if not validate_phone(phone):
        messagebox.showerror("Error", "Invalid phone number format")
        return

    conn = sqlite3.connect('employeemanagement.db')
    cursor = conn.cursor()
    cursor.execute('''UPDATE users SET name = ?, email = ?, phone = ?, position = ?, department = ?, address = ?
                      WHERE id = ?''', (name, email, phone, position, department, address, current_user_id))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Profile updated successfully")

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    pattern = r'^\d{10}$'
    return re.match(pattern, phone) is not None

def exit_profile():
    root.destroy()
    subprocess.Popen(["python", "dashboard.py"])

# Assume we get the user ID from the login process
current_user_id = 1  # This should be passed from the login or dashboard page

root = Tk()
# root.state("zoomed")
root.title("Employee Management System - User Profile")
root.config(bg="#1E2E56")

EMs = Label(text="Employee Management System", font=("Arial", 24, "bold"), bg="#1E2E56", fg="white")
EMs.place(x=610, y=13)

Userprofile = Label(text="User Profile", font=("Arial", 22, "bold"), bg="#1E2E56", fg="white")
Userprofile.place(x=700, y=90)

Name = Label(text="Name", bg="#1E2E56", fg="white", font=("Arial", 20))
Name.place(x=340, y=180)
Name_Entry = Entry(root, font=("Arial", 20))
Name_Entry.place(x=500, y=180)

Email = Label(text="Email", bg="#1E2E56", fg="white", font=("Arial", 20))
Email.place(x=340, y=260)
Email_Entry = Entry(root, font=("Arial", 20))
Email_Entry.place(x=500, y=260)

Phone = Label(text="Phone", bg="#1E2E56", fg="white", font=("Arial", 20))
Phone.place(x=340, y=340)
Phone_Entry = Entry(root, font=("Arial", 20))
Phone_Entry.place(x=500, y=340)

Position = Label(text="Position", bg="#1E2E56", fg="white", font=("Arial", 20))
Position.place(x=330, y=420)
Position_Entry = Entry(root, font=("Arial", 20))
Position_Entry.place(x=500, y=420)

Department = Label(text="Department", bg="#1E2E56", fg="white", font=("Arial", 20))
Department.place(x=310, y=500)
Department_Entry = Entry(root, font=("Arial", 20))
Department_Entry.place(x=500, y=500)

Address = Label(text="Address", bg="#1E2E56", fg="white", font=("Arial", 20))
Address.place(x=320, y=580)
Address_Entry = Entry(root, font=("Arial", 20))
Address_Entry.place(x=500, y=580)

Save_Button = Button(text="Save", font=("Arial", 20), command=save_user_data, bg="#4CAF50", fg="white")
Save_Button.place(x=900, y=700)

Exit = Button(text="Exit", font=("Arial", 20), command=exit_profile, bg="#f44336", fg="white")
Exit.place(x=1150, y=700)

# Load user data
user_data = load_user_data(current_user_id)
if user_data:
    Name_Entry.insert(0, user_data[4] if user_data[4] is not None else "")  # Name
    Email_Entry.insert(0, user_data[1] if user_data[1] is not None else "")  # Email
    Phone_Entry.insert(0, user_data[5] if user_data[5] is not None else "")  # Phone
    Position_Entry.insert(0, user_data[6] if user_data[6] is not None else "")  # Position
    Department_Entry.insert(0, user_data[7] if user_data[7] is not None else "")  # Department
    Address_Entry.insert(0, user_data[8] if user_data[8] is not None else "")  # Address
mainloop()
