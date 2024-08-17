from tkinter import *
from tkinter import messagebox
import sqlite3
import subprocess

def validate_login():
    username = Username_Entry.get()
    password = Password_Entry.get()

    if not username or not password:
        messagebox.showerror("Error", "Username and password are required")
        return

    conn = sqlite3.connect('employeemanagement.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    
    conn.close()

    if user:
        messagebox.showinfo("Success", "Login successful")
        root.destroy()  # Close the login window
        subprocess.Popen(["python", "dashboard.py"])  # Open the dashboard
    else:
        messagebox.showerror("Error", "Invalid username or password")

def forgotpassword():
    root.destroy()  # Close the login window
    subprocess.Popen(["python", "reset.py"])  # Open the dashboard

def open_registration_page():
    root.destroy()  # Close the login window
    subprocess.Popen(["python", "register.py"])  # Open the registration page

root = Tk()
root.title("Employee Management System")
root.config(bg="#1E2E56")
root.geometry("1200x700")  # Set a specific size for the window

EMs = Label(text="Employee Management System", font=("Arial", 24, "bold"), bg="#1E2E56", fg="white")
EMs.pack(pady=20)

frame = Frame(root, bg="#1E2E56")
frame.pack(expand=True)

Username = Label(frame, text="Username", bg="#1E2E56", fg="white", font=("Arial", 20))
Username.grid(row=0, column=0, padx=10, pady=10, sticky="e")

Username_Entry = Entry(frame, font=("Arial", 20))
Username_Entry.grid(row=0, column=1, padx=10, pady=10)

Password = Label(frame, text="Password", bg="#1E2E56", fg="white", font=("Arial", 20))
Password.grid(row=1, column=0, padx=10, pady=10, sticky="e")

Password_Entry = Entry(frame, font=("Arial", 20), show="*")
Password_Entry.grid(row=1, column=1, padx=10, pady=10)

button_frame = Frame(frame, bg="#1E2E56")
button_frame.grid(row=2, column=0, columnspan=2, pady=20)

login = Button(button_frame, text="Login", font=("Arial", 16), command=validate_login, bg="#4CAF50", fg="white")
login.pack(side=LEFT, padx=10)

Resetpassword = Button(button_frame, text="Reset Password", font=("Arial", 16), bg="#f44336", fg="white", command=forgotpassword)
Resetpassword.pack(side=LEFT, padx=10)

register = Button(button_frame, text="Register", font=("Arial", 16), command=open_registration_page, bg="#2196F3", fg="white")
register.pack(side=LEFT, padx=10)

mainloop()
